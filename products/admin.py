from django.contrib import admin

from project.mixins.admins import ImageSnapshotAdminMixin

from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    filter_horizontal = ('categories', 'products')

    # def get_image(self, obj): перенес в ImageSnapshotAdminMixin
    #     if obj.image:
    #         return format_html(
    #             '<img src="{}" width="64" height="64" />'.format(obj.image.url)
    #         )
    #     else:
    #         return ''
    # get_image.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description')

    # def get_image(self, obj): перенес в ImageSnapshotAdminMixin
    #     if obj.image:
    #         return format_html(
    #             '<img src="{}" width="64" height="64" />'.format(obj.image.url)
    #         )
    #     else:
    #         return ''
    #
    # get_image.short_description = 'Image'
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
