from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback


class FeedbackView(View):
    def get(self, request):
        form = FeedbackForm()
        return render(request, 'feedbacks/feedback.html', {'form': form})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('feedback')
        else:
            messages.error(request, 'Ошибка при добавлении отзыва. Пожалуйста, исправьте ошибки ниже.')
        return render(request, 'feedbacks/feedback.html', {'form': form})

