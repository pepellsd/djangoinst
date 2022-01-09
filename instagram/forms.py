from django import forms

from .models import Tag


class CreatePostForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple)
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={"class": "form-control", "maxlength": 500}))


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=500)

