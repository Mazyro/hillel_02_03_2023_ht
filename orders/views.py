from django.shortcuts import render


# Create your views here.
def orders(request, *args, **kwargs):
    # breakpoint()
    return render(request, 'orders/index.html')
