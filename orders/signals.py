from django.db.models.signals import post_save  # , m2m_changed
from django.dispatch import receiver
from orders.models import Order


# not needed due to external signals from DjangoLifeCircle
# @receiver(post_save, sender=Order)
# def set_order_price(sender, instance, **kwargs):
#     # breakpoint()
#     total_amount = instance.get_total_amount()
#     Order.objects.filter(id=instance.id).update(total_amount=total_amount)


# def order_item_changed(sender, instance, **kwargs):
#     # Do something
#     pass
#
# m2m_changed.connect(order_item_changed, sender=Order.order_items.through)
