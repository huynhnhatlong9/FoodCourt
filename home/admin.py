# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Food
from .models import User
from .models import Report
class FoodsAdmin(admin.ModelAdmin):
    list_display=['id','ten']
    list_filer=['ten']
 
class UserAdmin(admin.ModelAdmin):
    list_display=['user_name','password','user_type']

class ReportAdmin(admin.ModelAdmin):
    list_display=['user_name','food_buy','date']
# Register your models here.
admin.site.register(Food,FoodsAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Report,ReportAdmin)

