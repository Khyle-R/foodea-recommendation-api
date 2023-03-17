from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Foods, User, Orders
import json

@csrf_exempt
def recommend_articles(request):
    # Get the user's id in the request assuming the method is get
    request_user_id = request.GET.get('id')
    user = User.objects.get(user_id=request_user_id)

    # Get the recent orders of the user
    orders = Orders.objects.filter(customer_id=user.user_id).values('product_id')

    if orders.exists():
        count_orders = orders.count()
        print(count_orders)

        if count_orders > 5:
            orders = orders[:5]
            #put all the orders description, ingredients and name in a variable
            user_preference = ""
            for order in orders:
                temp_food = Foods.objects.get(product_id=order['product_id'])
                user_preference = user_preference + ' ' + temp_food.ingredients + ' ' + temp_food.description + ' ' + temp_food.product_name

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
            return JsonResponse({'recommended_foods': recommended_articles})
        else:
            return JsonResponse({'message': "User does not have enough data of orders. Recommendations can't proceed"})
    else:
        return JsonResponse({'message': "User have no orders yet. Recommendations can't proceed"})

    # print(user_preference)

    # if request.method == 'POST':
    #     # Get the user's article preferences from the API request
    #     preferences = json.loads(request.body)['preferences']

    #     # Create a TF-IDF vectorizer
    #     vectorizer = TfidfVectorizer(stop_words='english')

    #     # Get all the articles from the database
    #     articles = Foods.objects.all()

    #     # Create a TF-IDF matrix for the descriptiom
    #     article_matrix = vectorizer.fit_transform([article.ingredients + ' ' + article.description + ' ' + article.product_name for article in articles])

    #     # Create a TF-IDF vector for the user's preferences
    #     preferences_vector = vectorizer.transform([preferences])

    #     # Calculate the cosine similarity between the user's preferences and the articles
    #     similarity_scores = cosine_similarity(preferences_vector, article_matrix)

    #     # Find the top 5 most similar articles to the user's preferences
    #     similar_articles = similarity_scores.argsort()[0][::-1][:5]

    #    # Return the recommended articles as a JSON response
    #     recommended_articles = []
    #     # print(similar_articles)
    #     for i in similar_articles:
    #         article = articles[int(i)]
    #         # print(article_matrix)
    #         # article = Foods.objects.get(product_id=i+1)
    #         recommended_articles.append({
    #             'food_name': article.product_name,
    #             'food_description': article.description,
    #         })
    #     return JsonResponse({'recommended_foods': recommended_articles})
    # else:
    #     # Get the user's article preferences from the API request
    #     preferences = request.GET.get('preferences')

    #     # Create a TF-IDF vectorizer
    #     vectorizer = TfidfVectorizer(stop_words='english')

    #     # Get all the articles from the database
    #     articles = Foods.objects.all()

    #     # Create a TF-IDF matrix for the descriptiom
    #     article_matrix = vectorizer.fit_transform([article.ingredients + ' ' + article.description + ' ' + article.product_name for article in articles])

    #     # Create a TF-IDF vector for the user's preferences
    #     preferences_vector = vectorizer.transform([preferences])

    #     # Calculate the cosine similarity between the user's preferences and the articles
    #     similarity_scores = cosine_similarity(preferences_vector, article_matrix)

    #     # Find the top 5 most similar articles to the user's preferences
    #     similar_articles = similarity_scores.argsort()[0][::-1][:5]

    #    # Return the recommended articles as a JSON response
    #     recommended_articles = []
    #     # print(similar_articles)
    #     for i in similar_articles:
    #         article = articles[int(i)]
    #         # print(article_matrix)
    #         # article = Foods.objects.get(product_id=i+1)
    #         recommended_articles.append({
    #             'food_name': article.product_name,
    #             'food_description': article.description,
    #         })
    #     return JsonResponse({'recommended_foods': recommended_articles})
    #     # return JsonResponse({'message': 'This API endpoint only accepts POST requests'})

