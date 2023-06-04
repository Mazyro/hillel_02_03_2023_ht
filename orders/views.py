from django.shortcuts import render
from django.views import View

# rewritte in OOP
# def orders(request, *args, **kwargs):
#     # breakpoint()
#     return render(request, 'orders/index.html')


class OrdersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'orders/index.html')
