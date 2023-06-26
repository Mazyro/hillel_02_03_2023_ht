# from sqlite3 import register_converter
#
from django.urls.converters import UUIDConverter, StringConverter
from django.urls import path

from products.views import ProductsView, export_csv, \
    ExportToPdf, ImportCSV, export_csv_tameplate, AddOrRemoveFavoriteProduct


class UUIDConverter(StringConverter):  # noqa
    regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'


urlpatterns = [
    path('products/',
         ProductsView.as_view(),
         name='products'),
    path('products/export-csv/',
         export_csv,
         name='export_products_to_csv'),
    path('products/export-pdf/',
         ExportToPdf.as_view(),
         name='export_products_to_pdf'),
    path('products/import-csv/',
         ImportCSV.as_view(),
         name='products_from_csv'),
    path('products/export-csv-sample/',
         export_csv_tameplate,
         name='export_template_csv'),
    path('add_to_favourite/<uuid:pk>/',
         AddOrRemoveFavoriteProduct.as_view(),
         name='add_to_favourite'),
]
