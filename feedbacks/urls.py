from django.urls import path

from feedbacks.views import FeedbackView

urlpatterns = [

    path('feedback/', FeedbackView.as_view(), name='feedback'),
]