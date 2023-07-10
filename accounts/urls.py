from django.contrib.auth.views import LogoutView
from django.urls import path  # , include

from accounts.views import RegistrationView, LoginView, \
    ProfileView, PhoneCheckView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')), excluded
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('phone-check/', PhoneCheckView.as_view(), name='phone_check'),

]
