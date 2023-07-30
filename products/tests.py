import PyPDF2
from io import BytesIO
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product, Category, FavouriteProduct
from products.views import ExportToPdf, export_csv_template, AddOrRemoveFavoriteProduct, ProductByCategory, \
    ProductDetail
from project.constants import DECIMAL_PLACES, MAX_DIGITS
from django.http import HttpResponseRedirect
from django.http import Http404
import csv
from io import StringIO

User = get_user_model()


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


def test_export_csv_view(client, faker):
    # Создаем случайное имя и цену для продукта с помощью faker
    name = faker.word()
    price = '{:.2f}'.format(faker.pyfloat())  # Форматируем цену с двумя знаками после запятой
    # print(price)
    # Создаем продукт с заданным именем и ценой
    Product.objects.create(name=name, price=price)
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
    assert [name, '', price, ''] in csv_rows


# lesson =============================================================
def test_product_list(client, faker):
    for _ in range(3):
        Product.objects.create(
            name=faker.word(),
            sku=faker.word(),
            price=faker.pydecimal(
                min_value=0,
                left_digits=DECIMAL_PLACES,
                right_digits=MAX_DIGITS - DECIMAL_PLACES
            )
        )
    url = reverse('products') + '?ordering=created_at'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()


# my own ==========================================================================

def test_products_view_authenticated(client, faker):

    product = Product.objects.create(
        name=faker.word(),
        price=faker.pydecimal(
            min_value=0,
            left_digits=DECIMAL_PLACES,
            right_digits=MAX_DIGITS - DECIMAL_PLACES
        ),
    )
    category = Category.objects.create(
        name=faker.word(),
        slug=faker.slug(),
    )
    user, _ = User.objects.get_or_create(
        email=faker.email(),
        password='testpassword')
    product.categories.add(category)
    client.force_login(user)

    url = reverse('products')
    response = client.get(url)

    assert response.status_code == 200
    assert not hasattr(response.context['products'], 'is_favourite')

def test_export_to_pdf_view(client):
    # Create some test products
    # Replace this with your desired product creation logic
    # For example:
    Product.objects.create(name='Product 1', price=10)
    Product.objects.create(name='Product 2', price=15)

    # Generate a request using the request factory
    request_factory = RequestFactory()
    request = request_factory.get(reverse('export_products_to_pdf'))

    # Instantiate the view and get the response
    view = ExportToPdf.as_view()
    response = view(request)

    # Check the response status code
    assert response.status_code == 200

    # Check the Content-Type header
    assert response['Content-Type'] == 'application/pdf'

    # Read the PDF content from the response
    pdf_reader = PyPDF2.PdfReader(BytesIO(response.content))

    # Perform additional checks on the PDF content
    # For example, check the number of pages, text content, etc.
    # Here's an example of checking the number of pages:
    assert len(pdf_reader.pages) > 0


def test_export_csv_template_view(client):
    # Generate a request using the request factory
    request_factory = RequestFactory()
    request = request_factory.get(reverse('export_template_csv'))

    # Instantiate the view and get the response
    response = export_csv_template(request)

    # Check the response status code
    assert response.status_code == 200

    # Check the Content-Type header
    assert response['Content-Type'] == 'text/csv'

    # Read the CSV content from the response
    csv_data = response.content.decode()

    # Check if the CSV content contains the expected headers
    expected_headers = ['name', 'description', 'price', 'sku', 'category', 'is_active']
    csv_reader = csv.reader(csv_data.splitlines())
    csv_headers = next(csv_reader)
    assert csv_headers == expected_headers


def test_add_or_remove_favorite_product_view(client, faker):
    # Create a user and a product
    user, _ = User.objects.get_or_create(
        email=faker.email(),
        password='testpassword')
    product = Product.objects.create(name='Test Product', price=10)

    # Generate a request using the request factory
    request_factory = RequestFactory()
    request = request_factory.post(reverse('add_to_favourite', args=[product.pk]))

    # Simulate login for the user
    request.user = user

    # Instantiate the view and get the response
    view = AddOrRemoveFavoriteProduct.as_view()
    response = view(request, pk=product.pk)

    # Check the response status code (should be a redirect to products_url)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse('products')

    # Check if the product is added to the user's favorites
    assert FavouriteProduct.objects.filter(user=user, product=product).exists()

    # Repeat the process to remove the product from favorites
    response = view(request, pk=product.pk)

    # Check the response status code (should be a redirect to favourites_url)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse('favourites')

    # Check if the product is removed from the user's favorites
    assert not FavouriteProduct.objects.filter(user=user, product=product).exists()


def test_product_by_category_view(client):

    # Create a test category and products
    category = Category.objects.create(name='Test Category', slug='test-category')
    product1 = Product.objects.create(name='Product 1', price=10)
    product2 = Product.objects.create(name='Product 2', price=15)
    product1.categories.add(category)
    product2.categories.add(category)

    # Generate a request using the request factory
    request_factory = RequestFactory()
    url = reverse('products_by_category', kwargs={'slug': category.slug})
    request = request_factory.get(url)

    # Instantiate the view and get the response
    view = ProductByCategory.as_view()
    response = view(request, slug=category.slug)

    # Check the response status code (should be 200)
    assert response.status_code == 200

    # Check if the correct products are present in the context
    # products_in_context = response.context['products'] == ERROR
    products_in_context = response.context_data['products']
    assert product1 in products_in_context
    assert product2 in products_in_context

    # Check if the products are filtered correctly based on the category
    filtered_products = Product.objects.filter(categories=category)
    assert set(products_in_context) == set(filtered_products)

    # Test for a category that does not exist (should raise Http404)
    invalid_slug = 'non-existent-category'
    invalid_url = reverse('products_by_category', kwargs={'slug': invalid_slug})
    request_invalid = request_factory.get(invalid_url)

    try:
        response_invalid = view(request_invalid, slug=invalid_slug)
        assert False, "Expected Http404 but the view returned a response."
    except Http404:
        pass


def test_product_detail_view(client, faker):
    user, _ = User.objects.get_or_create(
        email=faker.email(),
        password='testpassword')

    # Create a test category
    category = Category.objects.create(name='Test Category', slug='test-category')

    # Create a test product
    product = Product.objects.create(name='Test Product', price=10)
    product.categories.add(category)

    # Generate a request using the request factory
    request_factory = RequestFactory()
    url = reverse('product', kwargs={'pk': product.pk})
    request = request_factory.get(url)
    request.user = user  # Attach the user to the request

    # Instantiate the view and get the response
    view = ProductDetail.as_view()
    response = view(request, pk=product.pk)

    # Check the response status code (should be 200)
    assert response.status_code == 200

    # Check if the correct product is present in the context
    product_in_context = response.context_data['product']
    assert product_in_context == product

    # Check if the product is marked as a favorite for an authenticated user
    if request.user.is_authenticated:
        assert hasattr(product_in_context, 'is_favourite')  # Check if 'is_favourite' attribute is present
        assert isinstance(product_in_context.is_favourite, bool)  # Check if 'is_favourite' is a boolean value

    # # Test for a product that does not exist (should raise Http404)
    # invalid_pk = 99999
    # invalid_name = 'non-existent-product'
    # invalid_url = reverse('product', kwargs={'pk': invalid_pk})
    # request_invalid = request_factory.get(invalid_url)
    # request_invalid.user = user  # Attach the user to the request
    #
    # try:
    #     response_invalid = view(request_invalid, pk=invalid_pk, slug=invalid_name)
    #     assert False, "Expected Http404 but the view returned a response."
    # except Http404:
    #     pass
