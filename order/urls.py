from django.urls import path
from payment import views as payment_view
from order import views as order_view

urlpatterns = [
    path('', order_view.cart_view, name='cart'),
    path('addMess/', order_view.cart_add_message, name='card-add-message'),
    path('reduce/<int:pk>/', order_view.cart_reduce, name='cart-reduce'),
    path('add/<int:pk>', order_view.cart_add, name='cart-add'),
    path('payment/', payment_view.payment, name='payment'),
    path('paydone/', payment_view.paydone, name='paydone'),
]
