from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView
from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback

from django.contrib.auth.mixins import UserPassesTestMixin


class FeedbackList(UserPassesTestMixin, ListView):
    model = Feedback
    template_name = 'feedbacks/feedback_list.html'
    context_object_name = 'feedbacks'
    # Сортировка по полю created_at в обратном порядке
    ordering = ['-created_at']

    # В данном примере используется UserPassesTestMixin,
    # который проверяет выполнение условия test_func для
    # доступа к представлению. Если test_func возвращает
    # False, то будет сгенерировано исключение PermissionDenied
    # и обработано ErrorHandlingMiddleware.
    def test_func(self):
        # Проверяем, является ли пользователь суперпользователем
        return self.request.user.is_superuser

    # В контексте примера с методом dispatch в FeedbackList,
    # мы переопределяем этот метод, чтобы добавить свою логику перед вызовом
    # метода представления. В данном случае, мы проверяем, является
    # ли пользователь суперпользователем, и если да, то
    # генерируем исключение. Если пользователь не является
    # суперпользователем, то вызывается супер-метод,
    # который выполняет стандартные действия представления.

    # Если нужно отключить генерацию исключения можна
    # просто добавить not в if с вызовом исключения:
    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            # Если пользователь суперпользователь, генерируем исключение
            raise Exception('Тестовое исключение')

        # Если пользователь не суперпользователь, вызываем супер-метод
        return super().dispatch(request, *args, **kwargs)


class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'feedbacks/index.html'
    success_url = reverse_lazy('feedbacks')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
