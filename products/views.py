from django.shortcuts import render


# Create your views here.


def products(requst, *args, **kwargs):
    # breakpoint()
    return render(requst, 'products/index.html')
