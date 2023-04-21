from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Foods, User, Orders, Favorites, ConsumedFood
from django.db.models.functions import TruncWeek
from django.db.models import Count
from django.db.models import Subquery, OuterRef, Sum, F, Value
import datetime
from datetime import timedelta
from django.utils import timezone
import json

@csrf_exempt
def recommend_articles(request):
    # Get the user's id in the request assuming the method is get
    request_user_id = request.GET.get('id')

    try:
        user = User.objects.get(user_id=request_user_id)

        current_user_calorie = calculate_today_calorie(user.user_id)
        preferred_calorie = calculate_user_preferred_calorie_per_day(user.user_id)

        remaining_calorie = preferred_calorie - current_user_calorie

        # Get the current date 
        # date = datetime.datetime.now()
        # today = date.strftime("%Y-%m-%d")

        # get the current date in the format of '%Y-%m-%d'
        


        # Get the recent orders of the user
        orders = Orders.objects.filter(customer_id=user.user_id, status="Delivered").values('product_id').order_by('-updated_at')

        # 

        if orders.exists():
            count_orders = orders.count()
            if count_orders > 5:
                orders = orders[:5]

                #put all the orders description, ingredients and name in a variable
                user_preference = ""
                for order in orders:
                    try:
                        temp_food = Foods.objects.get(product_id=order['product_id'])
                        user_preference = user_preference + ' ' + temp_food.ingredients + ' ' + temp_food.description + ' ' + temp_food.product_name
                    except Foods.DoesNotExist:
                        continue
                    
                #get the 10 recent favorites of user and add the info to the user preference
                favorites = Favorites.objects.filter(user_id=user.user_id).order_by('-updated_at')[:10]

                if favorites.exists():
                    for fav in favorites:
                        try:
                            favorite_id = fav.product_id
                            temp_food = Foods.objects.get(product_id=favorite_id)
                            user_preference = user_preference + ' ' + temp_food.ingredients + ' ' + temp_food.description + ' ' + temp_food.product_name
                        except Foods.DoesNotExist:
                            continue
                else:
                    pass

                # Create a TF-IDF vectorizer
                vectorizer = TfidfVectorizer(stop_words='english')

                # Get all the articles from the database
                articles = Foods.objects.filter(calories__lte=remaining_calorie)
                if(articles.count() < 10):
                    articles = Foods.objects.all()
                else:
                    pass

                # Create a TF-IDF matrix for the descriptiom
                article_matrix = vectorizer.fit_transform([article.ingredients + ' ' + article.description + ' ' + article.product_name for article in articles])

                # Create a TF-IDF vector for the user's preferences
                preferences_vector = vectorizer.transform([user_preference])

                # Calculate the cosine similarity between the user's preferences and the articles
                similarity_scores = cosine_similarity(preferences_vector, article_matrix)

                # Find the top 5 most similar articles to the user's preferences
                similar_articles = similarity_scores.argsort()[0][::-1][:5]

                # Return the recommended articles as a JSON response
                recommended_articles = []
                # print(similar_articles)
                for i in similar_articles:
                    article = articles[int(i)]
                    # print(article_matrix)
                    # article = Foods.objects.get(product_id=i+1)
                    recommended_articles.append({
                        'product_id' : article.product_id,
                        'merchant_id' : article.merchant_id,
                        'category_id' : article.category_id,
                        'product_name' : article.product_name,
                        'price' : article.price,
                        'calories' : article.calories,
                        'product_image' : article.product_image,
                        'stock' : article.stock,
                        'status' : article.status,
                        'description': article.description,
                        'date' : article.date
                    })
                return JsonResponse({'foods': recommended_articles})
            else:
                # recommendation will base on the user's preferences
                user_preference = user.preferences

                #get the 10 recent favorites of user and add the info to the user preference
                favorites = Favorites.objects.filter(user_id=user.user_id).order_by('-updated_at')[:10]

                if favorites.exists():
                    for fav in favorites:
                        try:
                            favorite_id = fav.product_id
                            temp_food = Foods.objects.get(product_id=favorite_id)
                            user_preference = user_preference + ' ' + temp_food.ingredients + ' ' + temp_food.description + ' ' + temp_food.product_name
                        except Foods.DoesNotExist:
                            continue
                else:
                    pass

                # Create a TF-IDF vectorizer
                vectorizer = TfidfVectorizer(stop_words='english')

                # Get all the articles from the database
                articles = Foods.objects.filter(calories__lte=remaining_calorie)
                if(articles.count() < 10):
                    articles = Foods.objects.all()
                else:
                    pass

                # Create a TF-IDF matrix for the descriptiom
                article_matrix = vectorizer.fit_transform([article.ingredients + ' ' + article.description + ' ' + article.product_name for article in articles])

                # Create a TF-IDF vector for the user's preferences
                preferences_vector = vectorizer.transform([user_preference])

                # Calculate the cosine similarity between the user's preferences and the articles
                similarity_scores = cosine_similarity(preferences_vector, article_matrix)

                # Find the top 5 most similar articles to the user's preferences
                similar_articles = similarity_scores.argsort()[0][::-1][:5]

                # Return the recommended articles as a JSON response
                recommended_articles = []
                # print(similar_articles)
                for i in similar_articles:
                    article = articles[int(i)]
                    # print(article_matrix)
                    # article = Foods.objects.get(product_id=i+1)
                    recommended_articles.append({
                        'product_id' : article.product_id,
                        'merchant_id' : article.merchant_id,
                        'category_id' : article.category_id,
                        'product_name' : article.product_name,
                        'price' : article.price,
                        'calories' : article.calories,
                        'product_image' : article.product_image,
                        'stock' : article.stock,
                        'status' : article.status,
                        'description': article.description,
                        'date' : article.date
                    })
                return JsonResponse({'foods': recommended_articles})
        else:
            # recommendation will base on the user's preferences
            user_preference = user.preferences
            
            # Create a TF-IDF vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')

            # Get all the articles from the database
            articles = Foods.objects.all()

            # Create a TF-IDF matrix for the descriptiom
            article_matrix = vectorizer.fit_transform([article.ingredients + ' ' + article.description + ' ' + article.product_name for article in articles])

            # Create a TF-IDF vector for the user's preferences
            preferences_vector = vectorizer.transform([user_preference])

            # Calculate the cosine similarity between the user's preferences and the articles
            similarity_scores = cosine_similarity(preferences_vector, article_matrix)

            # Find the top 5 most similar articles to the user's preferences
            similar_articles = similarity_scores.argsort()[0][::-1][:5]

            # Return the recommended articles as a JSON response
            recommended_articles = []
            # print(similar_articles)
            for i in similar_articles:
                article = articles[int(i)]
                # print(article_matrix)
                # article = Foods.objects.get(product_id=i+1)
                recommended_articles.append({
                    'product_id' : article.product_id,
                    'merchant_id' : article.merchant_id,
                    'category_id' : article.category_id,
                    'product_name' : article.product_name,
                    'price' : article.price,
                    'calories' : article.calories,
                    'product_image' : article.product_image,
                    'stock' : article.stock,
                    'status' : article.status,
                    'description': article.description,
                    'date' : article.date
                })
            return JsonResponse({'foods': recommended_articles})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist'})
    
def calculate_today_calorie(user):
    total_calories = 0
    date = datetime.datetime.now()
    today = date.strftime("%Y-%m-%d")
    # today = timezone.now().date()
 
    #check paid orders within the day
    today_orders = Orders.objects.filter(customer_id=user, status="Delivered", date=today)
    for order in today_orders:
        # try:
        #     food = Foods.objects.get(product_id=order.product_id)
        #     total_calories = total_calories + int(food.calories)
        # except Foods.DoesNotExist:
        #     continue
        try:
            food = Foods.objects.get(product_id=order.product_id)
            total_calories = total_calories + food.calories
        except Foods.DoesNotExist:
            continue
        # order_date = order.updated_at
        # converted_order_date = order_date.strftime("%Y-%m-%d")
        # if (converted_order_date == today):
        #     try:
        #         food = Foods.objects.get(product_id=order.product_id)
        #         total_calories = total_calories + int(food.calories)
        #     except Foods.DoesNotExist:
        #         continue
        # else:
        #     continue
    
    #check if user input items on the consumed food table
    other_foods = ConsumedFood.objects.filter(user_id=user, date=today)

    if other_foods.exists():
        for foods in other_foods:
            calories = foods.calories
            total_calories = total_calories + calories
    else:
        pass

    return total_calories

def weekly_average_calorie(user):
    orders_by_week = Orders.objects.filter(
        customer_id=user,
        status="Delivered"
    ).annotate(
        week=TruncWeek('date'),
    ).annotate(
        calories=Subquery(
            Foods.objects.filter(
                product_id=OuterRef('product_id')
            ).values('calories')[:1]
        )
    ).values('week', 'calories').annotate(
        count=Count('id')
    ).order_by('week')

    return orders_by_week

def get_calorie_of_product(id):
    calorie = 0
    food = Foods.objects.get(product_id=id)
    calorie = food.calories
    return calorie

def calculate_user_preferred_calorie_per_day(user):
    calorie_per_day = 0
    try:
        current_user = User.objects.get(user_id=user)
        if(current_user.gender == 'M'):
            bmr = (10 * current_user.weight) + (6.25 * current_user.height) - (5 * current_user.age) + 5
            if (current_user.lifestyle == 'A'):
                calorie_per_day = bmr * 1.2
            elif(current_user.lifestyle == 'B'):
                calorie_per_day = bmr * 1.375
            elif(current_user.lifestyle == 'C'):
                calorie_per_day = bmr * 1.55
            elif(current_user.lifestyle == 'D'):
                calorie_per_day = bmr * 1.725
            else:
                calorie_per_day = bmr * 1.9
        else:
            bmr = (10 * current_user.weight) + (6.25 * current_user.height) - (5 * current_user.age) - 161
            if (current_user.lifestyle == 'A'):
                calorie_per_day = bmr * 1.2
            elif(current_user.lifestyle == 'B'):
                calorie_per_day = bmr * 1.375
            elif(current_user.lifestyle == 'C'):
                calorie_per_day = bmr * 1.55
            elif(current_user.lifestyle == 'D'):
                calorie_per_day = bmr * 1.725
            else:
                calorie_per_day = bmr * 1.9
        return calorie_per_day
    except User.DoesNotExist:
        return calorie_per_day

def api_current_calorie(request):
    request_user_id = request.GET.get('id')
    try:
        user = User.objects.get(user_id=request_user_id)
        calorie = calculate_today_calorie(user.user_id)
        return JsonResponse({'current_calorie': calorie})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist'})
    
def api_weekly_calorie(request):
    weekly_average = {}
    request_user_id = request.GET.get('id')
    try:
        user = User.objects.get(user_id=request_user_id)

        total_calories = 0
        date = datetime.datetime.now()
        today = date.strftime("%Y-%m-%d")
        # today = timezone.now().date()
    
        for i in range(27):
            if i == 0:
                today_orders = Orders.objects.filter(customer_id=user.user_id, status="Delivered", date=today)
                if today_orders.exists():
                    for order in today_orders:
                        try:
                            food = Foods.objects.get(product_id=order.product_id)
                            total_calories = total_calories + (food.calories * order.quantity)
                        except Foods.DoesNotExist:
                            continue
                else:
                    pass
                #check if user input items on the consumed food table
                other_foods = ConsumedFood.objects.filter(user_id=user.user_id, date=today)

                if other_foods.exists():
                    for foods in other_foods:
                        calories = foods.calories
                        total_calories = total_calories + calories
                else:
                    pass
            else:
                if i == 6:
                    weekly_average.update({'this_week': total_calories})
                    total_calories = 0
                    continue
                elif i == 13:
                    weekly_average.update({'past_week': total_calories})
                    total_calories = 0
                    continue
                elif i == 20:
                    weekly_average.update({'past_week_2': total_calories})
                    total_calories = 0
                    continue
                elif i == 26:
                    weekly_average.update({'past_week_3': total_calories})
                    total_calories = 0
                    continue
                else:
                    yesterday = date - timedelta(days=i)
                    yesterday_str = yesterday.strftime("%Y-%m-%d")
                    today_orders = Orders.objects.filter(customer_id=user.user_id, status="Delivered", date=yesterday_str)
                    if today_orders.exists():
                        for order in today_orders:
                            try:
                                food = Foods.objects.get(product_id=order.product_id)
                                
                                total_calories = total_calories + (food.calories * order.quantity)
                            except Foods.DoesNotExist:
                                continue
                    else:
                        pass
                    #check if user input items on the consumed food table
                    other_foods = ConsumedFood.objects.filter(user_id=user.user_id, date=yesterday_str)

                    if other_foods.exists():
                        for foods in other_foods:
                            calories = foods.calories
                            total_calories = total_calories + calories
                    else:
                        pass
            
            

        # #check paid orders within the day
        # today_orders = Orders.objects.filter(customer_id=user, status="Delivered", date=today)
        # if today_orders.exists():
        #     for order in today_orders:
        #         try:
        #             food = Foods.objects.get(product_id=order.product_id)
        #             total_calories = total_calories + food.calories
        #         except Foods.DoesNotExist:
        #             continue
        # else:
        #     pass
        
        # #check if user input items on the consumed food table
        # other_foods = ConsumedFood.objects.filter(user_id=user, date=today)

        # if other_foods.exists():
        #     for foods in other_foods:
        #         calories = foods.calories
        #         total_calories = total_calories + calories
        # else:
        #     pass

        return JsonResponse(weekly_average)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist'})

def api_preferred_calorie(request):
    request_user_id = request.GET.get('id')
    try:
        user = User.objects.get(user_id=request_user_id)
        calorie = calculate_user_preferred_calorie_per_day(user.user_id)
        return JsonResponse({'preferred_calorie': calorie})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist'})
    
def home(request):
    return JsonResponse({'message': 'Nothing to see here'})
