from django.conf.urls import url

from menu import views

urlpatterns = [
    url('',views.MenuView.as_view(),name='menu')
]