from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from home.models import Food, User


class MenuView(ListView):
    model = Food
    template_name = 'menu/menu.html'
    context_object_name = 'long'
