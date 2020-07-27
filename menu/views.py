
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import  UpdateView
from home.models import Product, Cart, PayDone, OrderSuccess
from .filter import FoodFilter



def menu_view(request):
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
            messages.success(request, 'Đã thêm vào giỏ hàng!')
    context = {
        'foods': food,
        'filter': food_filter,
    }
    return render(request, 'menu/menu.html', context)


@login_required
def food_store(request):
    food = Product.objects.filter(shop_id=request.user.id)
    food_filter = FoodFilter(request.GET, queryset=food)
    food = food_filter.qs
    context = {
        'foods': food,
        'filter': food_filter,
    }
    return render(request, 'menu/foodstore.html', context)


def food_store_delete(request, pk):
    try:
        food = Product.objects.get(shop_id=request.user.id, id=pk)
        food.delete()
    finally:
        return redirect('foodstore')


class FoodUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'quantity']
    template_name = 'menu/foodstore-edit.html'
    success_url = reverse_lazy('foodstore')


def don_hang_view(request):
    if request.POST:
        try:
            obj = PayDone.objects.get(id=request.POST['pk'])
            OrderSuccess.objects.create(vendor=obj.vendor, customer=obj.customer, food=obj.food,
                                        quantity=obj.quantity, price=obj.price, date_done=timezone.now())
            obj.delete()
        finally:
            order = PayDone.objects.filter(vendor_id=request.user.id)
            context = {
                'orders': order
            }
            return render(request, 'menu/donhang.html', context)

    order = PayDone.objects.filter(vendor_id=request.user.id)
    context = {
        'orders': order
    }
    return render(request, 'menu/donhang.html', context)
