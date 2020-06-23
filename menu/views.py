from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from home.models import Product, Cart


class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category', 'image', 'price']


def menu_view(request):
    query = ''
    add = ''
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
        if 'add' in request.GET:
            add = request.GET['add']
            if Cart.objects.filter(food__id=add):
                Cart.objects.filter(food_id=add).update(
                    quantity=Cart.objects.get(food__id=add).quantity + 1)
            else:
                Cart.objects.create(user=request.user, food=Product.objects.get(id=add))
    food = Product.objects.filter(name__icontains=query)
    context = {
        'foods': food,
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
    context = {
        'foods': food,
    }
    return render(request, 'menu/cart.html', context)
