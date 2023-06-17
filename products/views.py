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
import weasyprint
import csv
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView
from products.forms import ProductModelForm, ImportCSVForm
from products.models import Product

from django.http import HttpResponse

from django.template.loader import render_to_string  # get_template,

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


class ProductsView(View):
    def get(self, request, *args, **kwargs):
        form = ProductModelForm()
        # exclude accessories
        products_list = Product.objects.exclude(categories__name='Accessories')
        return render(request, 'products/index.html', context={
            'products': products_list,
            'form': form,
            # 'key': request.key, для теста мидлвары TrackingMiddleware
        })

    def post(self, request, *args, **kwargs):
        form = ProductModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        # exclude accessories
        products_list = Product.objects.exclude(categories__name='Accessories')
        return render(request, 'products/index.html', context={
            'products': products_list,
            'form': form,

        })


def export_csv(request, *args, **kwargs):
    products_list = Product.objects.all()

    headers = {
        'Content-Tpe': 'text/csv',
        'Content-Disposition': 'attachment; filename="products.csv"'
    }
    fields_name = ['name', 'description', 'price', 'sku']
    response = HttpResponse(headers=headers)
    writer = csv.DictWriter(response, fieldnames=fields_name)
    writer.writeheader()

    for product in products_list:
        writer.writerow(
            {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'sku': product.sku
            }
        )
    return response


def export_csv_tameplate(request, *args, **kwargs):
    # products_list = Product.objects.all()

    headers = {
        'Content-Tpe': 'text/csv',
        'Content-Disposition': 'attachment; filename="products.csv"'
    }
    fields_name = [
        'name', 'description', 'price', 'sku', 'category', 'is_active'
    ]
    response = HttpResponse(headers=headers)
    writer = csv.DictWriter(response, fieldnames=fields_name)
    writer.writeheader()
    return response


class ExportToPdf(TemplateView):
    template_name = 'products/pdf.html'

    def get(self, request, *args, **kwargs):
        context = {'products': Product.objects.all()}
        headers = {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="products.pdf"'
        }
        html = render_to_string(
            template_name=self.template_name,
            context=context
        )
        pdf = weasyprint.HTML(string=html).write_pdf()
        response = HttpResponse(pdf, headers=headers)
        return response


# класс наследуется от FormView, который предоставляет функциональность
# для работы с формами.# Декораторы login_required и user_passes_test
# используются для проверки аутентификации пользователя и его статуса
# (должен быть сотрудником), чтобы разрешить доступ только
# авторизованным сотрудникам.
class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Метод form_valid вызывается, когда форма проходит валидацию,
    # и в нем вызывается form.save() для сохранения данных из CSV
    # файла в базе данных.Таким образом, код обрабатывает загрузку
    # CSV файла с продуктами, проверяет их корректность и сохраняет
    # в базе данных с помощью массовой операции bulk_create.
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
