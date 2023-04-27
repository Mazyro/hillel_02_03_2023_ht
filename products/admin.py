from django.contrib import admin

from project.mixins.admins import ImageSnapshotAdminMixin

from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    filter_horizontal = ('categories', 'products')


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')
