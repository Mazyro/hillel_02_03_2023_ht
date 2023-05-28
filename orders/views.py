from urllib import request

from django.shortcuts import render


class OrderView:
    def orders(self, *args, **kwargs):
        # breakpoint()
        return render(request, 'orders/index.html')
