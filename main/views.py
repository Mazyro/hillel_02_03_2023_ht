from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main/index.html'

    # Если нужно отключить генерацию исключения можна
    # просто закомментить строку с вызовом исключения:
    def get(self, request, *args, **kwargs):
        # Генерируем исключение для проверки обработки ошибок
        raise Exception('Тестовое исключение')

        # Если не нужно генерировать исключение,
        # можно просто вызвать супер-метод и откючить raise Exeption
        return super().get(request, *args, **kwargs)
