from django.urls import path, include
from . import views
from .forms import *

urlpatterns = [
    path('', views.home, name="home"),   
    path('home/', views.home, name = "home"),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('fotogallery/', views.fotogallery, name="fotogallery"),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('history/', views.history, name='history'),
    path('excursion/', views.excursion, name='excursion'),
]
