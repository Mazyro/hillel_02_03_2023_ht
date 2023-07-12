from django.contrib import admin
from project.mixins.admins import ImageSnapshotAdminMixin
from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'sku', 'categories_list', 'is_active')
    filter_horizontal = ('categories', 'products')

    def categories_list(self, obj):
        return ','.join(c.name for c in obj.categories.all())


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
