from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('welcome', views.welcome),
    path('logout', views.logout),
    path('login', views.login),
    path('add_book', views.add_book),
    path('add_fav/<int:book_id>', views.add_fav),
]