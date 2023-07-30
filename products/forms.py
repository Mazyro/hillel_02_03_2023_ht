import csv
import decimal
from io import StringIO
from django import forms
from products.models import Product, Category
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
        # Получаем загруженный файл из формы, используя self.cleaned_data.
        # cleaned_data содержит уже проверенные и очищенные данные из формы.
        csv_file = self.cleaned_data['file']

        # Создаем объект DictReader из модуля csv, чтобы прочитать содержимое
        # CSV файла. Мы используем StringIO для создания
        # файлоподобного объекта,
        # который позволяет нам передать содержимое файла
        # в DictReader.
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))

        # Пустой список перед циклом
        products_list = []

        for product in reader:
            try:
                # Получаем значение поля "category" из
                # текущей строки CSV файла.
                category_name = product['category']

                # Используя значение "category_name", мы вызываем
                # метод get_or_create()
                # для модели Category. Если категория с таким
                # именем уже существует,
                # get_or_create() вернет существующую категорию.
                # Если категория не существует, она будет создана.
                category, created = Category.objects.get_or_create(
                    name=category_name
                )

                sku = product['sku']
                # Выполняем запрос к базе данных, используя
                # filter() для поиска товара
                # с указанным SKU. Мы используем first() для получения первого
                # совпадающего товара, если он существует.
                existing_product = Product.objects.filter(sku=sku).first()

                # Проверяем, существует ли уже товар с указанным SKU.
                # continue: Если товар существует, идем далее пофайлу

                if existing_product:
                    # Товар уже существует, пропускаем его
                    continue
                # Создаем новый объект Product с данными из текущей
                # строки CSV файла.
                product_obj = Product(
                    name=product['name'],
                    description=product['description'],
                    price=decimal.Decimal(product['price']),
                    sku=sku,
                    is_active=product['is_active']
                )
                # Сохраняем созданный объект Product в базу данных.
                product_obj.save()
                # Добавляем связь между созданным товаром и категорией,
                # используя поле categories модели Product и метод add().
                product_obj.categories.add(category)
                # Добавляем созданный объект Product в список products_list.
                products_list.append(product_obj)
            except (KeyError, decimal.InvalidOperation) as err:
                raise ValidationError(err)
        if not products_list:
            raise ValidationError('Wrong file format.')
        return products_list

    def save(self):
        products_list = self.cleaned_data['file']  # no qa
        # убрал по-скольку есть уже сохранение
        # Product.objects.bulk_create(products_list)
        return products_list
