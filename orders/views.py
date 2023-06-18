from django.shortcuts import render  # , redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, RedirectView

from orders.mixins import GetCurrentOrderMixin
from orders.forms import CartForm, CartActionForm


# rewritte in OOP
# def orders(request, *args, **kwargs):
#     # breakpoint()
#     return render(request, 'orders/index.html')


class OrdersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'orders/index.html')

# Не получилось самому взял как у учителя
# class CartView(View):
#     form_class = CartForm
#     template_name = 'orders/cart.html'
#     success_url = None
#     def get(self, request):
#         # Логика получения содержимого корзины
#         # ...
#         # Заменить на свою логику получения товаров из корзины
#         # cart_items = []
#         cart_items = orders.order_items.all()
#           # Заменить на свою логику получения общей суммы корзины
#         cart_total = 0
#
#         return render(request, 'orders/cart.html', {
#             'cart_items': cart_items,
#             'cart_total': cart_total,
#         })
#
#
# class AddToCartView(View):
#     def post(self, request, product_id):
#         # Логика добавления товара в корзину
#         # ...
#
#         return redirect('cart')
#
#
# class RemoveFromCartView(View):
#     def post(self, request, cart_item_id):
#         # Логика удаления товара из корзины
#         # ...
#
#         return redirect('cart')
#
#
# class ApplyDiscountView(View):
#     def post(self, request):
#         # Логика применения скидки к корзине
#         # ...
#
#         return redirect('cart')
#
#
# class CheckoutView(View):
#     def post(self, request):
#         # Логика оформления заказа
#         # ...
#
#         return redirect('cart')


class CartView(GetCurrentOrderMixin, FormView):
    form_class = CartForm
    template_name = 'orders/cart.html'
    success_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context.update({
            'order': order,
            # 'order_items': order.order_items.all()
            'order_items': order.order_items.select_related('product').all()
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.get_object()})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CartActionView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('cart')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CartActionForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.action(kwargs.get('action'))
        return self.get(request, *args, **kwargs)
