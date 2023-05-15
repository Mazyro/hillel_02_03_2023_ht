from django.urls import path, include

from accounts.views import RegistrationView

# from accounts.views import LoginView, LogoutView

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),

    # we can use only this auth
    # Это добавит все необходимые URL-адреса для аутентификации Django,
    # такие как login, logout, password_change, password_reset и т.д.
    path('', include('django.contrib.auth.urls')),
    path('registration/', RegistrationView.as_view(), name='registration')
]
