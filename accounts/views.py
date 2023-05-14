# from django.views.generic import FormView, RedirectView
# from django.contrib.auth.forms import AuthenticationForm
#
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
