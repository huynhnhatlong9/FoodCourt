from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from order import views as order_view
from menu import views as menu_views

urlpatterns = [
    url('addfood/', login_required(order_view.AddFoodView.as_view()), name='addfood'),
    path('foodstore/delete/<int:pk>/', menu_views.food_store_delete, name='foodstore-delete'),
    path('foodstore/edit/<int:pk>/', menu_views.FoodUpdateView.as_view(), name='foodstore-edit'),
    url('foodstore/', login_required(menu_views.food_store), name='foodstore'),
    path('processing/', order_view.food_proccessing, name='food-processing'),
    url('', menu_views.menu_view, name='menu'),

]
