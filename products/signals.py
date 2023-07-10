from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
from products.models import Product


# @receiver(m2m_changed, sender=Product)
def product_categories_changed(sender, instance, **kwargs):
    # Do something
    # breakpoint()
    pass


m2m_changed.connect(
    product_categories_changed,
    sender=Product.categories.through
)
