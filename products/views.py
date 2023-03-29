from django.shortcuts import render

# Create your views here.
def products(requst, *args, **kwargs):
    return render(requst, 'products/index.html')
