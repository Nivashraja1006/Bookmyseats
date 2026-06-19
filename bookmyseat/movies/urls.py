from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail_view, name='movie_detail'),
]
