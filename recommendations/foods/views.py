from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Foods
import json

@csrf_exempt
def recommend_articles(request):
    if request.method == 'POST':
        # Get the user's article preferences from the API request
        preferences = json.loads(request.body)['preferences']

        # Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')

        # Get all the articles from the database
        articles = Foods.objects.all()

        # Create a TF-IDF matrix for the articles
        article_matrix = vectorizer.fit_transform([article.description for article in articles])

        # Create a TF-IDF vector for the user's preferences
        preferences_vector = vectorizer.transform([preferences])

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
                'title': article.product_name,
                'content': article.description,
            })
        return JsonResponse({'recommended_articles': recommended_articles})
    else:
        return JsonResponse({'message': 'This API endpoint only accepts POST requests'})

