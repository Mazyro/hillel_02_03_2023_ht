from django.urls import path

from main.views import MainView, ContactView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('contact/', ContactView.as_view(), name='contacts'),


]
