from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from home.models import Product, Cart
from .filter import FoodFilter


class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category', 'image', 'price']


def menu_view(request):
    add = ''
    food = Product.objects.all().filter(quantity__gt=0)
    food_filter = FoodFilter(request.GET, queryset=food)
    food = food_filter.qs
    if request.GET:
        if 'add' in request.GET:
            add = request.GET['add']
            obj = Cart.objects.filter(food_id=add, user_id=request.user.id)
            if obj:
                obj.update(quantity=obj.first().quantity + 1)
                obj = Cart.objects.all().get(food_id=add, user_id=request.user.id)
                obj.food.quantity -= 1
                obj.food.save()
            else:
                Cart.objects.create(user=User.objects.get(id=request.user.id), food=Product.objects.get(id=add))
                obj = Cart.objects.all().get(food_id=add, user_id=request.user.id)
                obj.food.quantity -= 1
                obj.food.save()
    context = {
        'foods': food,
        'filter': food_filter,
    }
    return render(request, 'menu/menu.html', context)


@login_required
def food_store(request):
    food = Product.objects.filter(shop_id=request.user.id)
    context = {
        'foods': food,
    }
    return render(request, 'menu/foodstore.html', context)


@login_required
def cart_view(request):
    food = Cart.objects.filter(user=request.user)
    if request.POST and food.count() > 0:
        if 'cl' in request.POST:
            cl = request.POST.get('cl')
            obj = Cart.objects.all().get(user=request.user, id=cl)
            if obj.quantity == 1:
                obj.food.quantity += 1
                obj.food.save()
                obj.delete()

            else:
                obj.quantity -= 1
                obj.save()
                obj.food.quantity += 1
                obj.food.save()
    food = Cart.objects.filter(user=request.user)
    context = {
        'foods': food,
    }
    return render(request, 'menu/cart.html', context)
