from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

        return ValidationError('User already exists')

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data[
            'email'
        ].split('@')[0]
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ===========================================================================
# new realization of views to be used, not need any more
# from django import forms
# from django.contrib.auth import authenticate
#
#
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args,**kwargs)
#         self.user = None
#
#     def clean(self):
#         self.user = authenticate(username=self.cleaned_data.get('username'),
#                                 password=self.cleaned_data.get('password'))
#         if self.user is None:
#             raise ValueError('Error')
#         return self.cleaned_data
