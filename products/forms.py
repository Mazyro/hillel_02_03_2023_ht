import csv
import decimal
from io import StringIO

from django import forms
from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from django.core.exceptions import ValidationError

from django.core.validators import FileExtensionValidator


class ProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=1000)
    price = forms.DecimalField(max_digits=MAX_DIGITS,
                               decimal_places=DECIMAL_PLACES
                               )
    sku = forms.CharField(max_length=25)
    image = forms.ImageField()

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid:
            if Product.objects.filter(name=self.cleaned_data['name']).exists():
                self.add_error('name', 'Product already exists')
                is_valid = False
        return is_valid

    def save(self):
        return Product.objects.create(**self.cleaned_data)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sku', 'image', 'price')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        if Product.objects.filter(name=self.cleaned_data['name']).exists():
            raise ValidationError('Product already exists')
        return self.cleaned_data['name']


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        # чтение и парсинг CSV файла с помощью csv.DictReader.
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
        products_list = []
        for product in reader:
            try:
                # создание экземпляров модели Product
                products_list.append(
                    Product(
                        name=product['name'],
                        description=product['description'],
                        price=decimal.Decimal(product['price']),
                        sku=product['sku'],
                        is_active=product['is_active']
                    )
                )
            except (KeyError, decimal.InvalidOperation) as err:
                raise ValidationError(err)
        if not products_list:
            raise ValidationError('Wrong file format.')
        return products_list

    # В методе save формы происходит массовое создание
    # записей продуктов с помощью Product.objects.bulk_create.
    def save(self):
        products_list = self.cleaned_data['file']
        Product.objects.bulk_create(products_list)
