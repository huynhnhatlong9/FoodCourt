from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from menu import views

urlpatterns = [
    url('addfood/', login_required(views.AddFoodView.as_view()), name='addfood'),
    url('foodstore/', login_required(views.food_store), name='foodstore'),
    url('', views.menu_view, name='menu'),
]
