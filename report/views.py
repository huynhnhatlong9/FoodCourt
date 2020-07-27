from django.forms import DateField
from home import models
from django.shortcuts import render
# Create your views here.
from home.models import OrderSuccess



# Create your views here.
def view_vendor(request):
    class Vendor:
        username=''
        count=0
        sales=0
        date_join=DateField
        def __init__(self,name,count,sales,date):
            self.username=name
            self.count=count
            self.sales=sales
            self.date_join=date
    vendors=[]
    list_vendor = models.User.objects.filter(is_staff=True, is_superuser=False)
    for vendor in list_vendor:
        vendors.append(Vendor(vendor.username,models.Product.get_num_of_product(models.Product,vendor.id),
                              models.OrderSuccess.get_sales(models.OrderSuccess,vendor.id),vendor.date_joined))
    contex = {
        'list_vendor': vendors
    }
    return render(request, 'report/vendor_view.html', contex)


def report_view(request):
    report = OrderSuccess.get_item_by_vendor(OrderSuccess, request.user.id)
    context = {
        'orders': report,
    }
    return render(request, 'report/report.html', context)


def customer_report_view(request):
    report = OrderSuccess.get_item_by_customer(OrderSuccess,request.user.id)
    context = {
        'orders': report,
    }
    return render(request, 'report/customer_report.html', context)

