# from django.db import models

from django.db import models

from django.contrib.auth import get_user_model
from products.models import Product

from django_lifecycle import LifecycleModelMixin
from project.mixins.models import PKMixin


User = get_user_model()


class FavouriteProduct(LifecycleModelMixin, PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='favourite_products'
    )
    group = models.CharField(max_length=255)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favourites'
    )

    class Meta:
        unique_together = ('product', 'user')
