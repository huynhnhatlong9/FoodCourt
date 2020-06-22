# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Product(models.Model):
    CATEGORY = (
        (0, 'Com'),
        (1, 'Bun'),
        (2, 'Pho'),
        (3, 'Mi'),
    )
    shop = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
        'is_staff': True
    }, default=True)
    category = models.IntegerField(choices=CATEGORY)
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('addfood')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_buy = models.DateTimeField()

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return self.user.username
