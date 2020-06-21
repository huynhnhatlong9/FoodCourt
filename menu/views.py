from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from home.models import Product, UserProfile


class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category']
