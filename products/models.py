# import uuid
from os import path
from django.core.validators import MinValueValidator
from django.db import models
from project.mixins.models import PKMixin


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


# Category (name, description, image, created_at, updated_at)
class Category(PKMixin):
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
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(PKMixin):

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
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # price = models.PositiveIntegerField()
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],  # for any classes
        max_digits=18,
        decimal_places=2
    )

    def __str__(self):
        return self.name

    # discount_type = models.CharField(
    #     choices=discount_type_choices, max_length=20
    # )
    # discount_value = models.DecimalField(
    # max_digits=5, decimal_places=2, default=0
    # )
    #
    # def get_discount_amount(self):
    #     if self.discount_type == DiscountType.PERCENT:
    #         return self.price * (self.discount_value / 100)
    #     elif self.discount_type == DiscountType.AMOUNT:
    #         return self.discount_value
    #     else:
    #         return 0
