
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email.split('@')[0]  # Генерация username из email
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.set_password(self.cleaned_data['password1'])  # Установка пароля
        if commit:
            user.save()
            if self.request:
                login(self.request, user)  # Автоматический вход после регистрации
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
#             raise ValueError('Errrroooorrr')
#         return self.cleaned_data
