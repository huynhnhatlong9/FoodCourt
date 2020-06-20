from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


class LoginView(LoginView):
    template_name = 'login/login.html'

