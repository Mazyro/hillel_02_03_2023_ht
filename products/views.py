# from django.shortcuts import render
#
# from products.forms import ProductModelForm
# from products.models import Product


# Create your views here.

# rewritte in OOP
# def products(request, *args, **kwargs):
#     if request.method == "POST":
#         form = ProductModelForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProductModelForm()
#     products_list = Product.objects.iterator()
#     return render(request, 'products/index.html', context={
#         'products': products_list,
#         'form': form,
#     })


from django.shortcuts import render
from django.views import View
from products.forms import ProductModelForm
from products.models import Product


class ProductsView(View):
    def get(self, request, *args, **kwargs):
        form = ProductModelForm()
        products_list = Product.objects.all()
        return render(request, 'products/index.html', context={
            'products': products_list,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        products_list = Product.objects.all()
        return render(request, 'products/index.html', context={
            'products': products_list,
            'form': form,
        })
