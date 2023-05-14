from django.urls import path, include

# from accounts.views import LoginView, LogoutView

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls'))
]
