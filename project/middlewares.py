from sys import exc_info
import traceback

from tracking.models import Tracking

from django.shortcuts import render


class TrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        # print("ERROR")
        # print(exc_info)
        _, _, _traceback = exc_info()
        tb = traceback.format_tb(_traceback)
        # breakpoint()
        Tracking.objects.create(
            method=request.method,
            url=request.path,
            data={
                'message': exception.args[0]
                if exception.args else 'Unknown Error',
                'traceback': tb,
                'get': request.GET,
                'post': request.POST

            }
        )
        return


# для примера брал переход на главную стр,
# если убрать raise exeption
# во вюь главной стр,
# то будет выполняться без генерации исключения, и эта middleware
# будет использоваться для обработки ошибок.
class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_exception(self, request, exception):
        # Здесь можна выполнить дополнительные действия
        # (записать информацию об ошибке в журнал,
        # отправить уведомление администратору и тд)

        # Возвращаем пользователю страницу с объяснением проблемы
        return render(request, 'products/error.html',
                      {'error_message': 'Произошла ошибка на '
                                        'сервере. Пожалуйста, '
                                        'попробуйте позже.'})
