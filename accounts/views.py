# Standard library imports
from datetime import timedelta

# Django imports
from django.conf import settings
from django.core import signing
from django.core.signing import TimestampSigner
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import (
    authenticate, get_user_model, login,
    logout, update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django import forms

# Local Django imports
from accounts.forms import (
    RegisterForm, UserForm, AvatarForm,
    UserEmailForm, SubscrForm, AccountClosureForm,
)
from accounts.models import tUserProfile


def register_view(request):
    """ Handle the registration of a new user. """

    # If the user is already logged in redirect him to the account page
    if request.user.is_authenticated():
        return redirect('/account/my-account/')
    else:
        # POST request
        if request.method == 'POST':
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                # Save the registration form
                user = register_form.save()
                # Refresh so that we can save to the additional tUserProfile
                user.refresh_from_db()
                user.tuserprofile.subscr = register_form.cleaned_data.get('subscr')
                # Get the password and authenticate the user
                password = register_form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=password)
                # Initialy set the user inactive.
                # He will receive an email with a link to activate the account
                user.is_active = False
                user.save()

                # Send the activation email
                user_id = user.id
                user_email = user.email
                send_email(receiver=user_email, id=user_id)

                return HttpResponse('<h4>See your email</h4>')
            else:
                messages.error(request, register_form.errors)
        # GET request
        else:
            register_form = RegisterForm()

        return render(request, 'accounts/register.html', {'register_form': register_form})

def activate_view(request):
    """ Handle the account activation of a newly registered user. """

    # Get the signed id string
    signed_id = request.GET.get('id')
    # Unsign it
    user_id = unsign_value(value=signed_id)

    # Don't like this error handling...
    # Needs to be fixed
    if user_id == -1:
        return HttpResponse('<h4>Signature has expired!</h4>')
    elif user_id == -2:
        return HttpResponse('<h4>Tampering detected!</h4>')

    user = User.objects.get(id=user_id)
    # Activate the user's account
    user.is_active = True
    user.save()
    return HttpResponse('<h4>Activation completed</h4>')

def my_account_view(request):
    """ Handle account changes. Check which form was passed by the request
        and update the account accordingly.
    """

    if request.user.is_authenticated():
        # POST request: Validate and save the forms.
        # Then render them with the new values pre-populated.
        if request.method == 'POST':

            which_form = request.POST.get('which_form')

            def checkUNA():
                """ Handle UNA updates. """

                user_form = UserForm(request.POST, instance=request.user)
                # We also need to post the avatar which lives in tUserProfile.
                # Create a new instance of AvatarForm.
                # Notice the request.FILES.
                # Django needs to know we are uploading a file.
                user_profile_form = AvatarForm(request.POST, request.FILES, instance=request.user.tuserprofile)

                if user_form.is_valid() and user_profile_form.is_valid():
                    user_form.save()
                    user_profile_form.save()
                    messages.success(request, 'Your account was updated successfully!')
                else:
                    messages.error(request, user_form.errors)

            def checkEmail():
                """ Handle Email updates. """

                user_email_form = UserEmailForm(request.POST, instance=request.user)

                if user_email_form.is_valid():
                    user_email_form.save()
                    messages.success(request, 'Your email was updated successfully!')
                else:
                    messages.error(request, user_email_form.errors)

            def checkSubscr():
                """ Handle Subscription changes. """

                # Create a new instance of the SubscrForm form
                subscr_form = SubscrForm(request.POST, instance=request.user.tuserprofile)

                if subscr_form.is_valid():
                    subscr_form.save()
                    messages.success(request, 'Your account was updated successfully!')
                else:
                    messages.error(request, subscr_form.errors)

            def checkPassword():
                """ Handle Password changes. """

                # PasswordChangeForm does not inherit from ModelForm
                password_form = PasswordChangeForm(user=request.user, data=request.POST)

                if password_form.is_valid():
                    user = password_form.save()
                    # The user should stay logged in after changing password.
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password was updated successfully!')
                else:
                    messages.error(request, password_form.errors)

            def checkClosure():
                """ Handle account closure. """

                account_closure_form = AccountClosureForm(request.POST, instance=request.user)

                if account_closure_form.is_valid():
                    account_closure_form.save()

            # Create a dictionary that maps the form name with a function
            options = {'UNAForm': checkUNA,
                       'EmailForm': checkEmail,
                       'SubscrForm': checkSubscr,
                       'PasswordForm': checkPassword,
                       'AccountClosureForm': checkClosure
            }

            options[which_form]()

            return redirect('/account/my-account/')

        # GET request: Render the forms, pre-populated with the existed values.
        else:
            user_form = UserForm(instance=request.user)
            user_profile_form = AvatarForm(instance=request.user.tuserprofile)
            user_email_form = UserEmailForm(instance=request.user)
            subscr_form = SubscrForm(instance=request.user.tuserprofile)
            password_form = PasswordChangeForm(user=request.user)
            account_closure_form = AccountClosureForm(instance=request.user)

        return render(request, 'accounts/my_account.html', {
            'user_form': user_form,
            'user_profile_form': user_profile_form,
            'user_email_form': user_email_form,
            'subscr_form': subscr_form,
            'password_form': password_form,
            'account_closure_form': account_closure_form
        })
    # If the user is not authenticated redirect him/her to the home page
    else:
        return redirect('/home/')

def login_view(request):
    """ Handle a login request """

    if request.user.is_authenticated():
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            # Default ModelBackend authentication is rejecting inactive users.
            # If the user is inactive then NONE will be returned instead
            if user is None:
                return HttpResponse('<h4>Invalid login</h4>')
            else:
                if user.is_active:
                    login(request, user)
                    return redirect('/home/')
        else:
            return redirect('/home/')

def logout_view(request):
    """ Handle a logout request """

    logout(request)
    return redirect('/home/')

def send_email(receiver, id):
    """ Send a confirmation email to a newly registered user.
        The email contains a signed URL to activate the account.

        Args:
            receiver: The email address of the user.
            id: The id of the user.
    """

    signed_id = sign_value(value=id)
    # Generate the activation URL
    activation_link = settings.DOMAIN_NAME + '/account/activate/?id=%s' % (signed_id)
    # Create additional context
    text = 'Thank you for registering!\nPlease follow the link below to activate your account:\n' + activation_link
    subject = 'Activate your account'
    # Send the email
    send_mail(
        subject,
        text,
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False,
    )

def sign_value(value):
    """ Cryptographically sign a value.
        Timestamp is also used to check expiration.

        Args:
            value: The value to be signed.
    """

    signer = TimestampSigner()
    value = signer.sign(value)
    return value

def unsign_value(value):
    """ Cryptographically unsign a value.
        Timestamp is also used to check expiration.

        Args:
            value: The value to be unsigned.
    """

    signer = TimestampSigner()
    try:
        value = signer.unsign(value, max_age=timedelta(seconds=settings.EMAIL_EXPIRATION_LIMIT))
        return value
    # SignatureExpired inherites from BadSignature
    except signing.SignatureExpired:
        return -1
    except signing.BadSignature:
        return -2