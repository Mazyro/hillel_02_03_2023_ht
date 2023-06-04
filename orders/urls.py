from django.urls import path

from orders.views import OrdersView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
]
