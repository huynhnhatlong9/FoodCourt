# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Category, Product, Cart
from .models import UserProfile
from .models import Report


class UserAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'food_buy', 'date']


# Register your models here.
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)