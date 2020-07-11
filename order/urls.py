from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from menu import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('addMess/', views.cart_add_message, name='card-add-message'),
    path('reduce/<int:pk>/', views.cart_reduce, name='cart-reduce'),
    path('add/<int:pk>', views.cart_add, name='cart-add'),
    path('payment/', views.payment, name='payment'),
]
