from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    PERCENT = 1, 'Percent'
    VALUE = 2, 'Value'


class OrderStatus(IntegerChoices):
    PENDING = 1, 'pending'
    CONFIRMED = 2, 'confirmed'
    SHIPPED = 3, 'shipped'
    DELIVERED = 4, 'delivered'
