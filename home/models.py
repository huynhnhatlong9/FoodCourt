# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Food(models.Model):
    ten = models.CharField(max_length=100)
    anh=models.ImageField(upload_to='media')
    gia=models.IntegerField()


class User(models.Model):
    user_name=models.CharField(max_length=100)
    password=models.TextField();
    user_type=models.CharField(max_length=10)

class Report(models.Model):
    user_name=models.CharField(max_length=100)
    food_buy=models.CharField(max_length=100)
    date=models.DateField();
