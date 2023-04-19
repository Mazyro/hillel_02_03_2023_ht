from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from enum import Enum


# добавил класс Enum
class DiscountType(Enum):
    PERCENT = 'percent'
    AMOUNT = 'amount'
    

discount_type_choices = [(tag.name, tag.value) for tag in DiscountType]


class Discount(PKMixin):

    discount_type = models.CharField(choices=discount_type_choices, max_length=20)  # заменил по совету учителя
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

    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
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

    def calculate_total_price(self):
        total_price = sum([item.calculate_price_with_discount()
                           for item in self.items.all()])
        discount_amount = self.calculate_discount_amount()

        return total_price - discount_amount

    def calculate_discount_amount(self):
        discount_amount = 0

        for discount in self.discounts.all():
            if discount.discount_type == 'percent':
                discount_amount += (self.calculate_total_price()
                                    * (discount.discount_value / 100))
            else:
                discount_amount += discount.discount_value

        return discount_amount


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

    @property
    def total_price(self):
        return self.price * self.quantity

    def calculate_price_with_discount(self):
        discount_amount = self.calculate_discount_amount()
        return self.total_price - discount_amount

    def calculate_discount_amount(self):
        discount_amount = 0

        for discount in self.discounts.all():
            if discount.discount_type == 'percent':
                discount_amount += (self.total_price *
                                    (discount.discount_value / 100))
            else:
                discount_amount += discount.discount_value

        return discount_amount
