from django.conf.urls import url

from menu import views

urlpatterns = [
    url('',views.AddFoodView.as_view(),name='menu')
]