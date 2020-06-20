from home.models import Food as foods


def context(request):
    return {
        'list': foods.objects.all(),
    }
