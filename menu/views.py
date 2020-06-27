from pprint import pprint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from home.models import Product, Cart
from .filter import FoodFilter


class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category', 'image', 'price', 'quantity']

    def form_valid(self, form):
        self.object = form.save()
        self.object.shop = self.request.user
        return super().form_valid(form)


def menu_view(request):
    add = ''
    food = Product.objects.all().filter(quantity__gt=0)
    food_filter = FoodFilter(request.GET, queryset=food)
    food = food_filter.qs
    if request.POST:
        if 'add' in request.POST:
            add = request.POST['add']
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


def cart_reduce(request, pk):
    try:
        food = Cart.objects.get(id=pk)
        food.food.quantity += food.quantity
        food.food.save()
        food.delete()
        food = Cart.objects.filter(user=request.user)
        context = {
            'foods': food,
        }
        return render(request, 'menu/cart.html', context)
    finally:
        food = Cart.objects.filter(user=request.user)
        return redirect('cart')


def cart_add(request, pk):
    try:
        food = Cart.objects.get(id=pk)
        if food.food.quantity > 0:
            food.food.quantity -= 1
            food.quantity += 1
            food.food.save()
            food.save()
        food = Cart.objects.filter(user=request.user)
        context = {
            'foods': food,
        }
        return render(request, 'menu/cart.html', context)
    finally:
        return redirect('cart')


def payment(request):
    food = Cart.objects.filter(user=request.user)
    sum={
        'price': 0,
        'quantity':0,
    }
    for x in food:
        sum['price']+=x.food.price
        sum['quantity']+=x.quantity

    context = {
        'sum':sum,
        'foods': food,
    }
    return render(request, 'menu/payment.html', context)


def food_store_delete(request, pk):
    pprint(request.user.id)
    try:
        food = Product.objects.get(shop_id=request.user.id, id=pk)
        food.delete()
    finally:
        return redirect('foodstore')


class FoodUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price','quantity']
    template_name = 'menu/foodstore-edit.html'
    success_url = reverse_lazy('foodstore')
