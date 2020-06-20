# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Food


# Create your views here.
def index(request):
    list_food = Food.objects.filter()
    return render(request, 'home/home.html', {
        'list_food': list_food,
    })
