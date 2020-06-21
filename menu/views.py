from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from home.models import Product, UserProfile


class MenuView(ListView):
    model = Product
    template_name = 'menu/menu.html'
    context_object_name = 'long'
