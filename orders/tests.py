from django.urls import reverse


# Тестирование OrdersView:
def test_orders_view(client):
    url = reverse('orders')
    response = client.get(url)
    assert response.status_code == 200
    assert 'orders/index.html' in [t.name for t in response.templates]
