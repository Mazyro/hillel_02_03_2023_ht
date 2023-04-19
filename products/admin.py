from django.contrib import admin
from django.utils.html import format_html
# from django.utils.safestring import mark_safe
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'name', 'price', 'is_active')
    filter_horizontal = ('categories', 'products')

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="64" height="64" />'.format(obj.image.url)
            )
        else:
            return ''
    get_image.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ist_display = ('name', 'description', 'get_image')

    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="64" height="64" />'.format(obj.image.url)
            )
        else:
            return ''

    get_image.short_description = 'Image'
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
