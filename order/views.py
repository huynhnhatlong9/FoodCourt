from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from home.models import Product, Cart, PayDone


# Create your views here.
class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category', 'image', 'price', 'quantity']

    def form_valid(self, form):
        self.object = form.save()
        self.object.shop = self.request.user
        return super().form_valid(form)


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
        messages.success(request, f"Trả Thành Công!")
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
        messages.success(request, f"Trả Thành Công!")
        return render(request, 'menu/cart.html', context)
    finally:
        food = Cart.objects.filter(user=request.user)
        messages.success(request, f"Trả Thành Công!")
        return redirect('cart')


@csrf_exempt
def cart_add_message(request):
    if request.is_ajax():
        pk = request.POST.get('pk', None)
        text = request.POST.get('text', None)
        try:
            obj = Cart.objects.get(id=pk)
            obj.notice = text
            obj.save()
            print(obj.notice)
        except:
            None
        return JsonResponse({}, status=200)


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
        messages.success(request, f"Thêm Thành Công!")
        return render(request, 'menu/cart.html', context)
    finally:
        messages.success(request, f"Thêm Thành Công!")
        return redirect('cart')


def food_proccessing(request):
    foods = PayDone.get_item_by_customer(PayDone, request.user.id)
    return render(request, 'menu/dangxuli.html', {
        'foods': foods
    })
