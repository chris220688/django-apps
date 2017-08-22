from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import (
	ModelForm,
	CharField,
	BooleanField
)
from django.forms.widgets import FileInput, TextInput, PasswordInput
from django.contrib.auth.models import User
from accounts.models import tUserProfile

##########################
#   Registration forms   #
##########################

# Create a registration form
# These values come both from auth_user and tUserProfile tables
class RegisterForm(UserCreationForm):
	# Give some additional special CSS attributes to each field
	username   = CharField(widget=TextInput(attrs={'placeholder': 'Username*', 'class': "form-control"}),required=True)
	email      = CharField(widget=TextInput(attrs={'placeholder': 'Email*', 'class': "form-control"}),required=True)
	password1  = CharField(widget=PasswordInput(attrs={'placeholder': 'Password*', 'class': "form-control"}),required = True)
	password2  = CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm Password*', 'class': "form-control"}),required = True)
	first_name = CharField(widget=TextInput(attrs={'placeholder': 'First Name', 'class': "form-control"}),required=False)
	last_name  = CharField(widget=TextInput(attrs={'placeholder': 'Last Name', 'class': "form-control"}),required=False)
	subscr     = BooleanField(required=False)

	class Meta:
		model   = User
		fields  = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'subscr']

##########################
# Account Settings forms #
##########################

# Create a form for username, first_name, last_name
# These values live in auth_user table
class UserForm(ModelForm):
    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name']

# Create a form for the avatar
# This value lives in tUserProfile which extends auth_user table
class AvatarForm(ModelForm):
	class Meta:
		model   = tUserProfile
		fields  = ['avatar']
		# The widget will help us get rid of the default labels
		widgets = {
			'avatar': FileInput()
		}

# Create a form for the Email
class UserEmailForm(ModelForm):
	class Meta:
		model  = User
		fields = ['email']

# Create a form for the subscription
# This value lives in tUserProfile which extends auth_user table
class SubscrForm(ModelForm):
	class Meta:
		model  = tUserProfile
		fields = ['subscr']

# Create a form for the account closure
class AccountClosureForm(ModelForm):
	class Meta:
		model  = User
		fields = ['is_active']