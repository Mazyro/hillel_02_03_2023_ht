from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import OrderItem


@receiver(post_save, sender=OrderItem)
def set_order_item_price(sender, instance, **kwargs):
    if instance.product:
        instance.price = instance.product.price
