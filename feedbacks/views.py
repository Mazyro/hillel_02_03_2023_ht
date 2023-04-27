from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from feedbacks.forms import FeedbackForm


class FeedbackView(LoginRequiredMixin, View):
    form_class = FeedbackForm
    template_name = 'feedbacks/index.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            # привязываем отзыв к залогиненому пользователю
            feedback.user = request.user
            feedback.save()
            # перенаправляем на страницу успешной отправки отзыва
            return redirect('feedbacks/feedback_success')

        return render(request, self.template_name, {'form': form})
