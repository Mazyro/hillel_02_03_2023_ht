from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login
from django.views.generic import CreateView
# from accounts.forms import RegistrationForm, AuthenticationForm
# from project import settings
from django.urls import reverse_lazy
from accounts.forms import RegistrationForm, AuthenticationForm
# from django.views.generic import FormView, UpdateView, RedirectView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("profile")

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


class LoginView(AuthLoginView):
    form_class = AuthenticationForm


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        verification_code = request.POST.get('verification_code')

        # Провалидировать номер телефона и проверить код
        if self.check_verification_code(verification_code):
            # Действия после успешной валидации
            # ...

            # Обновить модель пользователя
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.is_phone_valid = True
            user.save()

            messages.success(
                request, 'Phone number is needed to be verified'
            )
            return redirect('login')
        else:
            messages.error(
                request, 'Invalid phone number or verification code.'
            )
            return redirect('profile')

    def check_verification_code(self, verification_code):
        # Проверка кода верификации
        return verification_code == '1234'

    def phone_is_valid(self, phone):
        # Провалидировать номер телефона
        # .....
        return True  # Измените на свою логику валидации номера телефона
