from django import forms
from django.utils.html import strip_tags
from .models import Feedback


class FeedbackForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Feedback
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']
        text = strip_tags(text)
        return text
