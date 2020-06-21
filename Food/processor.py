from home.models import Product as foods


def context(request):
    return {
        'list': foods.objects.all(),
    }
