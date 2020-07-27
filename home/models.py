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

    def is_available(self):
        return self.quantity > 0

    def get_item_by_vendor(self, vendor_id):
        try:
            return self.objects.filter(shop_id=vendor_id)
        except:
            return None

    def get_num_of_product(self, vendor_id):
        try:
            return self.objects.filter(shop_id=vendor_id).count()
        except:
            return None


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_buy = models.DateTimeField(default=datetime.now())
    notice = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return self.user.username

    def get_item_by_customer(self, customer_id):
        try:
            return self.objects.filter(user_id=customer_id)
        except:
            return None

    def get_item_by_foodname(self, foodname):
        try:
            return self.objects.filter(food=foodname)
        except:
            return None


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
    notice = models.TextField(blank=True, default='')

    def __str__(self):
        return self.food

    class Meta:
        ordering = ('-date_pay',)

    def get_item_by_id(self, id):
        try:
            return self.objects.get(id=id)
        except:
            return None

    def get_item_by_customer(self, customer_id):
        try:
            return self.objects.filter(customer_id=customer_id)
        except:
            return None

    def get_item_by_vendor(self, vendor_id):
        try:
            return self.objects.filter(vendor_id=vendor_id)
        except:
            return None

    def get_item_by_name(self, name):
        try:
            return self.objects.filter(food=name)
        except:
            return None

    def get_item_by_price(self, price):
        try:
            return self.objects.filter(price=price)
        except:
            return None


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

    class Meta:
        ordering = ('-date_done',)

    def __str__(self):
        return self.food

    def get_item_by_id(self, id):
        try:
            return self.objects.get(id=id)
        except:
            return None

    def get_item_by_customer(self, customer_id):
        try:
            return self.objects.filter(customer_id=customer_id)
        except:
            return None

    def get_item_by_vendor(self, vendor_id):
        try:
            return self.objects.filter(vendor_id=vendor_id)
        except:
            return None

    def get_item_by_name(self, name):
        try:
            return self.objects.filter(food=name)
        except:
            return None

    def get_item_by_price(self, price):
        try:
            return self.objects.filter(price=price)
        except:
            return None
    def get_sales(self,vendor_id):
        try:
            count=0
            obj=self.objects.filter(vendor_id=vendor_id)
            for o in obj:
                count+=o.quantity
            return count
        except:
            return None