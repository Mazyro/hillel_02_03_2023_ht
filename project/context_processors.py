from orders.models import Order
from products.models import Category
from django.core.cache import cache


# def slug_categories(request) -> dict:
#     slugs = Category.objects.values('slug', 'name')
#     return {'category_slugs': slugs}
def slug_categories(request) -> dict:
    slugs = cache.get('category_slugs')
    print(f'{slugs} from cache')
    if slugs is None:
        slugs = Category.objects.values('slug', 'name')
        cache.set('category_slugs', slugs)
        print(f'{slugs} not cache')
    return {'category_slugs': slugs.order_by('name'),
            'is_home': request.path == f'/{request.LANGUAGE_CODE}/'
            }


# def products_in_cart(request) -> dict:
#     active_order = cache.get('items_in_cart')
#     if active_order is None:
#         active_order = Order.objects.filter(is_active=True)
#         cache.set('items_in_cart', active_order)
#     number_product = len(active_order.values('order_items'))
#     return {'items_in_cart': number_product}

