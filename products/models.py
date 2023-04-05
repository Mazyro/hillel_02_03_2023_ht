import uuid
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


# Product (name, description, image, created_at, updated_at, price (positive integer field), sku (char field))
class Product(PKMixin):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


# Discount (amount (positive integer field), code (char field), is_active (boolean field, default=True),
# discount_type (choices (0, 'В деньгах'), (1, 'Проценты') подумайти какой тип у поля и почему))
# class Discount(models.Model):
#     amount = models.PositiveIntegerField()
#     code = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     DISCOUNT_CHOICES = (
#         (0, 'amount'),
#         (1, 'percent'),
#     )
#     discount_type = models.IntegerField(choices=DISCOUNT_CHOICES)
