# import uuid
from os import path
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db import models
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import StatusModel
from project.model_choices import Currencies, ProductCacheKeys
from currencies.models import get_euro_rate, get_usd_rate
from django_lifecycle import LifecycleModelMixin, hook, \
    AFTER_UPDATE, AFTER_CREATE, BEFORE_UPDATE, BEFORE_CREATE

from django.core.cache import cache

User = get_user_model()


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    is_manual_slug = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,  # empty to Django
        null=True  # empty to db
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when='name', has_changed=True)
    def after_signal(self):
        if not self.is_manual_slug:
            self.slug = slugify(self.name)


class Product(LifecycleModelMixin, PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,  # empty to Django
        null=True  # empty to db
    )
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True
    )
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],  # for any classes
        max_digits=18,
        decimal_places=2
    )
    currency = models.CharField(
        choices=Currencies.choices,
        default=Currencies.UAH,
        max_length=16
    )
    price_uah = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    @hook(AFTER_UPDATE, when_any=['currency', 'price'], has_changed=True)
    @hook(AFTER_CREATE)
    def set_price_uah(self):
        self.price_uah = self.get_price_uah()
        self.save(update_fields=('price_uah',), skip_hooks=True)

    def __str__(self):
        return f"{self.name} --- Price {self.price_uah}"

    def get_price_uah(self):
        price_uah = self.price
        if self.currency == 'EUR':
            price_uah = self.price * get_euro_rate()
        elif self.currency == 'USD':
            price_uah = self.price * get_usd_rate()
        return price_uah

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_signal(self):
        cache.delete(ProductCacheKeys.PRODUCTS)


class FavouriteProduct(StatusModel):
    STATUS = Choices('active', 'inactive')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = StatusField(default=STATUS.active)

    class Meta:
        verbose_name = 'Favourite Product'
        verbose_name_plural = 'Favourite Products'

    def __str__(self):
        return f'{self.product.sku}'

    def is_favourite(self):
        return self.status
