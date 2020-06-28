# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Product(models.Model):
    CATEGORY = (
        (0, 'Cơm'),
        (1, 'Bún'),
        (2, 'Phở'),
        (3, 'Bánh Mì'),
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
    quantity = models.IntegerField(default=1)

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
    quantity = models.IntegerField(default=1)
    date_buy = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return self.user.username


class PayDone(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, limit_choices_to={
        'is_staff': False
    }, related_name='customer')
    vendor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, limit_choices_to={
        'is_staff': True
    }, related_name='vendor')
    food = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_pay = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.food

    class Meta:
        ordering = ('-date_pay',)


class OrderSuccess(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, limit_choices_to={
        'is_staff': False
    }, related_name='customer_order')
    vendor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, limit_choices_to={
        'is_staff': True,
    }, related_name='vendor_order')
    food = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_done = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.food
