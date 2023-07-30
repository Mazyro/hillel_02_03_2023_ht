from django import forms
from feedbacks.models import Feedback
from django.utils.html import escape
import bleach


class FeedbackForm(forms.ModelForm):
    # Meta класс в модели формы позволяет определить какие поля
    # модели необходимо включить в форму и как их отображать.
    # В данном конкретном случае Meta класс определяет, что форма
    # будет построена на основе модели Feedback и будет иметь
    # поля text user raiting, так как они указаны в списке полей fields.
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def clean_text(self):
        text = self.cleaned_data['text']
        # очистка от специальных символов
        text = escape(text)
        # очистка от html
        text = bleach.clean(text, strip=True)
        return text

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        self.fields['rating'].help_text = "Rating should be" \
                                          " from 1 to 5 points."
