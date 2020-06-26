from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from menu import views

urlpatterns = [
    url('addfood/', login_required(views.AddFoodView.as_view()), name='addfood'),
    path('foodstore/delete/<int:pk>/', views.food_store_delete, name='foodstore-delete'),
    path('foodstore/edit/<int:pk>/', views.FoodUpdateView.as_view(), name='foodstore-edit'),
    url('foodstore/', login_required(views.food_store), name='foodstore'),
    url('', views.menu_view, name='menu'),
]
