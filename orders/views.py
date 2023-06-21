from django.shortcuts import render  # , redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, RedirectView

from orders.mixins import GetCurrentOrderMixin
from orders.forms import CartForm, CartActionForm
from django.http import HttpResponseRedirect


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


# представление, отображающее корзину и обрабатывающее форму
class CartView(GetCurrentOrderMixin, FormView):
    #: указывает класс формы, используемой представлением,
    # в данном случае - CartForm.
    form_class = CartForm
    template_name = 'orders/cart.html'
    # : указывает URL, на который будет перенаправлен

    # метод-хук, применяющий декоратор login_required
    # для требования аутентификации пользователя
    # перед доступом к представлению.
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #  метод, возвращающий URL для перенаправления
    #  пользователя после успешной обработки формы.
    def get_success_url(self):
        return reverse('cart')

    #  метод, возвращающий контекст данных для
    #  передачи в шаблон.
    #  Он добавляет объект order и связанные с ним
    #  объекты order_items в контекст.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        cart_items_count = order.order_items.count() if order else 0
        context.update({
            'order': order,
            # 'order_items': order.order_items.all()
            'order_items': order.order_items.select_related('product').all(),
            'cart_items_count': cart_items_count
        })
        return context

    # метод, возвращающий аргументы для создания
    # экземпляра формы. В данном случае,
    # он добавляет instance (текущий заказ) в аргументы формы.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.get_object()})
        return kwargs

    # метод, вызываемый при успешной валидации формы.
    # Он сохраняет данные формы с помощью метода save() формы.
    def form_valid(self, form):
        # breakpoint()
        form.save()
        return super().form_valid(form)


#  представление, обрабатывающее действия в корзине,
#  такие как добавление товара,
#  удаление товара, очистка корзины и оплата.
#  Оно также наследуется от GetCurrentOrderMixin и RedirectView
class CartActionView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('products')

    #  метод-хук, применяющий декоратор login_required
    #  для требования аутентификации пользователя перед доступом
    #  к представлению
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #  метод, обрабатывающий POST-запросы.
    #  Он создает экземпляр формы CartActionForm с переданными данными POST
    #  и текущим заказом, а затем вызывает метод action() формы,
    #  передавая действие (action) из параметров запроса.
    def post(self, request, *args, **kwargs):
        form = CartActionForm(request.POST, instance=self.get_object())
        # Если форма валидна, то выполняется
        # соответствующее действие (add, pay, remove, clear).
        if form.is_valid():
            action = self.kwargs['action']
            if action == 'remove':
                form.action(kwargs.get('action'))
                return HttpResponseRedirect(reverse('cart'))
        form.action(kwargs.get('action'))
        return self.get(request, *args, **kwargs)
