from django import forms
from django.forms import ModelForm, CharField
from blog.models import tComment
from django.forms.widgets import HiddenInput, Textarea

class CommentForm(ModelForm):

	text  = CharField(widget=Textarea(attrs={'placeholder': 'Add a comment...', 'class': 'form-control', 'rows': '3'}),required=True)

	class Meta:
		model  = tComment
		fields = ['post', 'text']
		widgets = {
			'post': forms.HiddenInput()
		}