# Django imports
from django import forms
from django.forms import (
    ModelForm, CharField
)
from django.forms.widgets import (
    HiddenInput, Textarea
)

# Local Django imports
from blog.models import tComment


class CommentForm(ModelForm):
    """ Creates a comments form """

    text = CharField(widget=Textarea(attrs={'placeholder': 'Add a comment...', 'class': 'form-control', 'rows': '3'}),
        required=True
    )

    class Meta:
        model = tComment
        fields = ['post', 'text']
        widgets = {
            'post': forms.HiddenInput()
        }