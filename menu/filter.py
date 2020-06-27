import django_filters
from django_filters import FilterSet

from home.models import Product


class FoodFilter(FilterSet):
    name=django_filters.CharFilter(label='Name: ',lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name','category']