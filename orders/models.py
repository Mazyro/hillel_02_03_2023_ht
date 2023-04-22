# from django.contrib.auth.models import User
# так делать нельзя, мы не моем быть уверены что юзер
# именно в этой модели, для этого нужна следующая строка

from django.contrib.auth import get_user_model
# и затем
# User = get_user_model() в строке 16

from django.core.validators import MinValueValidator
from django.db import models
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.choices import DiscountTypes
from django.utils import timezone


User = get_user_model()


# добавил класс Enum
# class DiscountType(Enum):
#     PERCENT = 'percent'
#     AMOUNT = 'amount'
#
#
# discount_type_choices = [(tag.name, tag.value) for tag in DiscountType]


class Discount(PKMixin):

    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    code = models.CharField(
        max_length=32,
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )
    discount_value = models.DecimalField(
        max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, default=0
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"

    @property
    def is_valid(self):
        is_valid = self.is_active
        if self.valid_until:
            is_valid &= timezone.now() <= self.valid_until
        return is_valid


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

# ддля валидации уникальности is_active=True и юзера, тоесть
    # проверяем что  данного юзера только один активный ордер
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    def calculate_total_price(self):
        total_price = 0
        # for item in self.items.all(): -> ...  items.iterator():
        # for item in self.items.all():
        for item in self.items.iterator():  # лучше итерироавться
            if item.discount_type == DiscountTypes.PERCENT:
                item_price = item.price * (100 - item.discount_value) / 100
            elif item.discount_type == DiscountTypes.VALUE:
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
