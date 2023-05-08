from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.utils.html import escape
import bleach
from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback
from django.utils.decorators import method_decorator


class FeedbackList(ListView):
    model = Feedback
    template_name = 'feedbacks/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10


class FeedbackView(CreateView):
    @method_decorator(login_required)
    def get(self, request):
        form = FeedbackForm(request.GET)
        return render(request, 'feedbacks/feedback.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.text = escape(form.cleaned_data['text'])  # очистка от специальных символов
            feedback.text = bleach.clean(feedback.text, strip=True)  # очистка от html
            feedback.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('feedbacks')
        else:
            messages.error(request, 'Ошибка при добавлении отзыва. Пожалуйста, исправьте ошибки ниже.')
        return render(request, 'feedbacks/feedback.html', {'form': form})


# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.generic import ListView, CreateView
#
# from feedbacks.forms import FeedbackForm
# from feedbacks.models import Feedback
#
#
# class FeedbackView(CreateView):
#     form_class = FeedbackForm
#     template_name = 'feedbacks/feedback.html'
#     success_url = reverse_lazy('feedbacks')
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({'user': self.request.user})
#         return kwargs
#
#
# class FeedbackList(ListView):
#     template_name = 'feedbacks/feedback_list.html'
#     model = Feedback
