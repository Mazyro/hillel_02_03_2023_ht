from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount', 'order_number', 'total_amount')
    # filter_horizontal = ('categories', 'products')


@admin.register(OrderItem)
class CategoryAdmin(admin.ModelAdmin):
    ist_display = ('product', 'quantity', 'price', 'is_active')
