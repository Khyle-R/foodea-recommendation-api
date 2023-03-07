from django.urls import path
from .views import recommend_articles

urlpatterns = [
    path('recommendations/', recommend_articles, name='recommend_articles'),
]