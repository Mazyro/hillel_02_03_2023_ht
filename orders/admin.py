from django.contrib import admin

from orders.models import Order, OrderItem, Discount


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user',  'order_number', 'total_amount')
    # filter_horizontal = ('categories', 'products')


@admin.register(OrderItem)
class CategoryAdmin(admin.ModelAdmin):
    ist_display = ('product', 'quantity', 'price', 'is_active')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'discount_type')

