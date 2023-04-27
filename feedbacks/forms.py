
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Feedback
        fields = ['text', 'rating']

    def clean_text(self):
        text = self.cleaned_data['text']
        # Очистка текста от специальных символов и т.д.
        return text

    def save(self, user):
        feedback = super().save(commit=False)
        feedback.user = user
        feedback.save()
        return feedback
