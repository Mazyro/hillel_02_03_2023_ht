import uuid
from os import path

from django.db import models


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


# Product (name, description, image, created_at, updated_at, price (positive integer field), sku (char field))
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Category (name, description, image, created_at, updated_at)
class Category(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Discount (amount (positive integer field), code (char field), is_active (boolean field, default=True),
# discount_type (choices (0, 'В деньгах'), (1, 'Проценты') подумайти какой тип у поля и почему))
class Discount(models.Model):
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    DISCOUNT_CHOICES = (
        (0, 'В деньгах'),
        (1, 'Проценты'),
    )
    discount_type = models.IntegerField(choices=DISCOUNT_CHOICES)
