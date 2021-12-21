from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')