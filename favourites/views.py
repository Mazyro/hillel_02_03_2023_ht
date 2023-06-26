from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from favourites.models import FavouriteProduct
from products.models import Product


class FavouriteProductList(ListView):
    model = FavouriteProduct
    template_name = 'favourites/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AddOrRemoveFavoriteProduct(DetailView):
    model = Product

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        favourite, created = FavouriteProduct.objects.get_or_create(
            product=self.object,
            user=request.user
        )
        if not created:
            favourite.delete()
        return HttpResponseRedirect(reverse_lazy('products'))
