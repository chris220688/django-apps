# Django imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import (
    ModelForm, CharField, BooleanField,
)
from django.forms.widgets import FileInput, TextInput, PasswordInput

# Local Django imports
from accounts.models import tUserProfile


class RegisterForm(UserCreationForm):
    """ Creates a registration form.
        These values come both from auth_user and tUserProfile tables
    """

    # Give some additional special CSS attributes to each field
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username*', 'class': 'form-control'}),
        required=True)
    email = CharField(widget=TextInput(attrs={'placeholder': 'Email*', 'class': 'form-control'}),
        required=True)
    password1 = CharField(widget=PasswordInput(attrs={'placeholder': 'Password*', 'class': 'form-control'}),
        required = True)
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': 'Confirm Password*', 'class': 'form-control'}),
        required = True)
    first_name = CharField(widget=TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
        required=False)
    last_name = CharField(widget=TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
        required=False)
    subscr = BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'subscr']

class UserForm(ModelForm):
    """ Creates a form for username, first_name, last_name.
        These values live in auth_user table.
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class AvatarForm(ModelForm):
    """ Creates an form for the avatar.
        This value lives in tUserProfile which extends auth_user table.
    """

    class Meta:
        model = tUserProfile
        fields = ['avatar']
        # The widget will help us get rid of the default labels
        widgets = {
            'avatar': FileInput()
        }

class UserEmailForm(ModelForm):
    """ Creates a form for the email """

    class Meta:
        model  = User
        fields = ['email']

class SubscrForm(ModelForm):
    """ Creates a form for the subscription option.
        This value lives in tUserProfile which extends auth_user table.
    """

    class Meta:
        model = tUserProfile
        fields = ['subscr']

class AccountClosureForm(ModelForm):
    """ Creates a form for the account closure option. """

    class Meta:
        model = User
        fields = ['is_active']
