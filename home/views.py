# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request, 'home/home.html')

def intro_view(request):
    return render(request, 'home/intro.html')
