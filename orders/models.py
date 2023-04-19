from enum import Enum

from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


# User = get_user_model() # I dont know why it needed?


# добавил класс Enum
class DiscountType(Enum):
    PERCENT = 'percent'
    AMOUNT = 'amount'


discount_type_choices = [(tag.name, tag.value) for tag in DiscountType]


class Discount(PKMixin):

    discount_type = models.CharField(
        choices=discount_type_choices, max_length=20
    )  # заменил по совету учителя
    discount_value = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )
    is_active = models.BooleanField(
        default=True
    )
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )
    code = models.CharField(max_length=255)


class Order(PKMixin):

    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order_number = models.CharField(max_length=255)

    total_amount = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    def __str__(self):
        return f"Order №{self.order_number} " \
               f"Amount: {self.total_amount}. User: {User}"

# для уникальности юзера
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    def calculate_total_price(self):
        total_price = 0
        for item in self.items.all():
            if item.discount_type == DiscountType.PERCENT:
                item_price = item.price * (100 - item.discount_value) / 100
            elif item.discount_type == DiscountType.AMOUNT:
                item_price = item.price - item.discount_value
            else:
                item_price = item.price

            total_price += item_price * item.quantity

        return total_price


class OrderItem(PKMixin):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='items'
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    is_active = models.BooleanField(default=True)
    discounts = models.ManyToManyField(
        Discount, blank=True, related_name='order_items'
    )

    def __str__(self):
        return f"Order Item - {self.product} "

# для уникальности заказа
    class Meta:
        unique_together = ('order', 'product')
