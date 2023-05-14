from django.urls import path

from feedbacks.views import FeedbackView, FeedbackList

urlpatterns = [
    path('', FeedbackList.as_view(), name='feedbacks'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]
