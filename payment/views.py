from django.db.models.functions import datetime
from django.shortcuts import render
# Create your views here.
from home.models import Cart, PayDone
from payment.momo import momo_payment


# Create your views here.

def payment(request):
    food = Cart.objects.filter(user=request.user)
    sum = {
        'price': 0,
        'quantity': 0,
    }
    for x in food:
        sum['price'] += x.food.price * x.quantity
        sum['quantity'] += x.quantity

    if request.POST:
        return momo_payment(request, sum['price'])
    context = {
        'sum': sum,
        'foods': food,
    }
    return render(request, 'menu/payment.html', context)


def paydone(request):
    if request.GET:
        print('return\n')
        print(request.GET)
        r = request.GET.get('errorCode')
        if r == '0':
            text = 'Thành công'
            try:
                food = Cart.objects.filter(user_id=request.user.id)
                for x in food:
                    PayDone.objects.create(customer=x.user, vendor=x.food.shop, food=x.food.name, quantity=x.quantity,
                                           price=x.food.price, date_pay=datetime.datetime.now(), notice=x.notice)
                food.delete()
            except:
                None
        else:
            text = 'Thất bại'
    return render(request, 'menu/paydone.html', {
        'text': text
    })
