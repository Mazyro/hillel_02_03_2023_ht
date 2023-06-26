from django.urls import path

from favourites.views import FavouriteProductList


urlpatterns = [
    path('', FavouriteProductList.as_view(), name='favourites'),
]
