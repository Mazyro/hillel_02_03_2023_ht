from django.urls import reverse


# Тестирование OrdersView:
def test_orders_view(client):
    url = reverse('orders')
    response = client.get(url)
    assert response.status_code == 200
    assert 'orders/index.html' in [t.name for t in response.templates]


#  фикстуры передаются в camel_case с нижним подч,
def test_cart_view(client, login_client, product_factory, faker):
    url = reverse('cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context['order_items']
    order = response.context['order']
    assert order
    assert not order.order_items.exists()

    product = product_factory()

    data = {
        'product_id': product.pk  # Use the ID of the created product
    }
    response = client.post(reverse('cart_action', args=('add',)), data=data, folow=True)
    assert response.status_code == 302
    assert order.order_items.exists()
    # breakpoint()
