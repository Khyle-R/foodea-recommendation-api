"""foodea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommendations import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommendations/', views.recommend_articles, name='recommend_articles'),
    path('current_calorie/', views.api_current_calorie, name='api_current_calorie'),
    path('preferred_calorie/', views.api_preferred_calorie, name='api_preferred_calorie'),
    path('weekly_calorie/', views.api_weekly_calorie, name='api_weekly_calorie')
]
