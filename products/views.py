from urllib import request

from django.shortcuts import render

from products.forms import ProductModelForm
from products.models import Product


class ProductsView:

    def products(self, *args, **kwargs):
        if request.method == "POST":
            form = ProductModelForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
        else:
            form = ProductModelForm()
        products_list = Product.objects.iterator()
        return render(request, 'products/index.html', context={
            'products': products_list,
            'form': form,
        })
