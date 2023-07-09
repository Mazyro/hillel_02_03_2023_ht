from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from main.forms import ContactForm
# from django.core.mail import mail_admins
from django.utils.translation import gettext_lazy as _
from project.celery import send_email_task


class MainView(TemplateView):
    template_name = 'main/index.html'

    # Если нужно отключить генерацию исключения можна
    # просто закомментить строку с вызовом исключения:
    def get(self, request, *args, **kwargs):
        # Генерируем исключение для проверки обработки ошибок
        # raise Exception('Тестовое исключение')

        # Если не нужно генерировать исключение,
        # можно просто вызвать супер-метод и откючить raise Exeption
        return super().get(request, *args, **kwargs)


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contacts/index.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        # can send html-messages instead common messages
        msg = f'FROM: ' \
              f'{form.cleaned_data["email"]}\n{form.cleaned_data["text"]}'
        text = _('Contact form')
        # mail_admins(text, msg)
        send_email_task.apply_async((text, msg), retry=False)
        return super().form_valid(form)
