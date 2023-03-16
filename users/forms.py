from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'biography',
            'category',
            'profile_pic'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError([f'This username {username} has already existed.'])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, strip=True)
    password = forms.CharField(max_length=150, strip=True, widget=forms.PasswordInput)
