from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User, Tag


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')


class UserEditForm(UserChangeForm):
    password = None
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'cols': 10}))

    class Meta:
        model = User
        exclude = ["email", "password"]
        fields = ["first_name", "last_name", "bio", "avatar"]


class CreatePostForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={"class": "form-control", "maxlength": 500}))



class UploadUserImagesForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="select Image")
