import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes
from django_lifecycle import AFTER_SAVE, hook, \
    AFTER_UPDATE

User = get_user_model()


class Discount(PKMixin):
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
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
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.discount_value} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"

    # проверяем на то чтобы акция была актуальной
    @property
    def is_valid(self):
        is_valid = self.is_active
        if self.valid_until:
            is_valid &= (timezone.now() <= self.valid_until)
        return is_valid


class Order(PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    order_number = models.PositiveSmallIntegerField(default=1)

    # UniqueConstraint, который гарантирует, что у
    # каждого пользователя (user) может быть только
    # один активный заказ.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    def __str__(self):
        return f"User: {self.user}  " \
               f"Total amount: {self.total_amount}  " \
               f"Discount: ({ self.discount })"

    # Это свойство (property), которое определяет,
    # является ли заказ текущим. Заказ считается
    # текущим, если он активен (is_active=True)
    # и не оплачен (is_paid=False).
    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        total_amount = self.order_items.aggregate(
            total_amount=Sum(F('price') * F('quantity'))
        )['total_amount'] or 0
        total_amount = decimal.Decimal(total_amount)
        if self.discount and self.discount.is_valid:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (total_amount / 100 * self.discount.amount)
            ).quantize(decimal.Decimal('.01'))
        return total_amount

    #  Это метод-хук (hook), который вызывается после
    #  обновления заказа.
    #  Он обновляет поле total_amount вызовом метода
    #  get_total_amount()
    #  и сохраняет изменения, пропуская хуки, чтобы
    #  избежать рекурсивных вызовов.
    # убрал skip_hooks=True в save по скольку была оошибка
    # Model.save() got an unexpected keyword argument 'skip_hooks'
    @hook(AFTER_UPDATE, when='discount', has_changed=True)
    def set_total_amount(self):
        self.total_amount = self.get_total_amount()
        self.save(update_fields=('total_amount',), )


class OrderItem(PKMixin):
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='order_items',
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    # Это внутренний класс Meta, который
    # определяет уникальность пары полей order и product.
    # Это гарантирует, что каждый товар в заказе является уникальным.
    class Meta:
        unique_together = ('order', 'product')

    # Это свойство (property), которое вычисляет
    # подытог для данного товара. Оно умножает
    # цену товара на количество и возвращает результат.
    @property
    def sub_total(self):
        return self.product.price * self.quantity

    # Это метод-хук (hook), который вызывается после
    # сохранения товара в заказе.
    # Он обновляет общую сумму заказа, вызывая метод get_total_amount()
    # у связанного объекта order и сохраняет изменения, пропуская хуки,
    # чтобы избежать рекурсивных вызовов.
    @hook(AFTER_SAVE)
    def set_order_total_amount(self):
        self.order.total_amount = self.order.get_total_amount()
        self.order.save(update_fields=('total_amount',), skip_hooks=True)
