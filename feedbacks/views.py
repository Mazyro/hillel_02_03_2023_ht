# from pyexpat.errors import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from django.views.generic import ListView, CreateView
# from django.utils.html import escape
# import bleach
from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class FeedbackList(ListView):
    model = Feedback
    template_name = 'feedbacks/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10


class FeedbackView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedbacks/feedback.html'
    success_url = reverse_lazy('feedbacks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.instance.text = bleach.clean(form.instance.text, strip=True)
        return super().form_valid(form)


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
