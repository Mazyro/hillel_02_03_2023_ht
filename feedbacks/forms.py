from django import forms
from feedbacks.models import Feedback


class FeedbackForm(forms.ModelForm):
    # Meta класс в модели формы позволяет определить какие поля
    # модели необходимо включить в форму и как их отображать.
    # В данном конкретном случае Meta класс определяет, что форма
    # будет построена на основе модели Feedback и будет иметь
    # поля text user raiting, так как они указаны в списке полей fields.
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user
        self.fields['rating'].help_text = "Rating should be" \
                                          " from 1 to 5 points."
