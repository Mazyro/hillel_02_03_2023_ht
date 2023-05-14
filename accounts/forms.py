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
