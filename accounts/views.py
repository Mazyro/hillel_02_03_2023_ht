from django.contrib.auth import login
from django.views.generic import CreateView

from accounts.forms import RegistrationForm

from project import settings


class RegistrationView(CreateView):
    form_class = RegistrationForm

    template_name = 'registration/registration.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# этому коду не место во вью, все должно быть в форме - замечание учителя
    # def form_valid(self, form):
    #     # Сохраняем пользователя в базу
    #     user = form.save(commit=False)
    #     user.username = user.email.split('@')[0]
    #     user.is_active = True
    #     user.is_staff = False
    #     user.is_superuser = False
    #     user.set_password(form.cleaned_data.get('password'))
    #     user.save()
    #
    #     # Авторизуем пользователя
    #     login(self.request, user)
    #     return redirect(self.success_url)

# new realization to be used
# from django.views.generic import FormView, RedirectView
# from django.contrib.auth.forms import AuthenticationForm#
# from accounts.forms import LoginForm
# from django.contrib.auth import login, logout
#
#
# class LoginView(FormView):
#     template_name = 'accounts/login.html'
#     form_class = AuthenticationForm
#     # success_url = '/'  - так нельзя заменям на метод
#
#     def get_success_url(self):
#         return self.request.GET.get('next')
#
#     # убрали из зто того что заменили TemplateView  на  FormView
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context.update({'form': LoginForm()})
#     #     return context
#
#     # заменили
#     # def post(self, request, *args, **kwargs):
#     #     # breakpoint()
#     #     next_redirect = request.GET.get('next')
#     #     form = self.form_class(data=request.POST)
#     #     if form.is_valid():
#     #         login(request, form.user)
#     #         return redirect(next_redirect)
#     #     return self.get(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super().form_valid(form)
#
#
# class LogoutView(RedirectView):
#     url = '/feedbacks/' # временно
#
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return super().get(request, *args, **kwargs)
