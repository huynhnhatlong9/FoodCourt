
from django_filters import FilterSet

from home.models import Product


class FoodFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'name': ['exact']
        }