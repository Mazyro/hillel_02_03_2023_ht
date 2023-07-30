from django.contrib import admin

from orders.models import Order, OrderItem, Discount
from django.contrib.admin import TabularInline


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_number', 'total_amount')
    # filter_horizontal = ('categories', 'products')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price', 'is_active', 'order')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'discount_type')
