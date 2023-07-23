
from django.urls import reverse
from products.models import Product, Category


# def test_product_detail_view(client):
#     product = Product.objects.create(name='Test Product', price=10)
#     url = reverse('product-detail', kwargs={'pk': product.pk})
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.context['product'] == product


def test_products_view(client):
    category = Category.objects.create(name='Test Category', slug='test-category')
    product = Product.objects.create(name='Test Product', price=10)
    product.categories.add(category)
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert product in response.context['products']


import csv
from io import StringIO

def test_export_csv_view(client):
    Product.objects.create(name='Test Product 1', price=10)
    Product.objects.create(name='Test Product 2', price=15)

    url = reverse('export_products_to_csv')
    response = client.get(url)

    # Устанавливаем тип содержимого вручную
    response['Content-Type'] = 'text/csv'

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/csv'

    # Анализируем CSV-файл
    csv_data = response.content.decode()
    csv_reader = csv.reader(StringIO(csv_data))
    csv_rows = list(csv_reader)

    # Проверяем, что заголовки полей присутствуют
    assert csv_rows[0] == ['name', 'description', 'price', 'sku']

    # Проверяем, что продукты присутствуют в CSV-файле
    assert ['Test Product 1', '', '10.00', ''] in csv_rows
    assert ['Test Product 2', '', '15.00', ''] in csv_rows
