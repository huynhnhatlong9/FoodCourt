from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from home.models import Product


class AddFoodView(CreateView):
    model = Product
    template_name = 'menu/addfood.html'
    fields = ['name', 'category', 'image', 'price']


def menu_view(request):
    query = ''
    if request.GET:
        query = request.GET['q']

    food = Product.objects.filter(name__icontains=query)
    context = {
        'foods': food,
    }
    return render(request, 'menu/menu.html', context)


def food_store(request):
    food = Product.objects.filter(shop_id=request.user.id)
    context = {
        'foods': food,
    }
    return render(request, 'menu/foodstore.html', context)
