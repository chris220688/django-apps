from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.models import tUserProfile
from django.http import HttpResponse
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	update_session_auth_hash
)
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from accounts.forms import (
	RegisterForm,
	UserForm,
	AvatarForm,
	UserEmailForm,
	SubscrForm,
	AccountClosureForm
)
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from datetime import timedelta
from django.core.signing import TimestampSigner
from django.core import signing


# This view is handling the registration of a new user
def register_view(request):

	# If the user is already logged in redirect him to the account page
	if request.user.is_authenticated():
		return redirect('/account/my-account/')
	else:
		# If this is a POST request, add the new user details in the DB and log him in
		if request.method == 'POST':
			register_form = RegisterForm(request.POST)

			if register_form.is_valid():
				# Save the registration form
				user = register_form.save()
				# Refresh so that we can save to the additional tUserProfile table
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
				user_id    = user.id
				user_email = user.email
				send_email(user_email, user_id)

				return HttpResponse('<h4>See your email</h4>')
			else:
				messages.error(request, register_form.errors)
		# If this is a GET request return a blank registration form
		else:
			register_form = RegisterForm()

		return render(request, 'accounts/register.html', {'register_form': register_form})

# This function sends confirmation email to a newly registered user
# The email contains a signed URL to activate the account 
def send_email(receiver, id):
	# Cryptographically sign the id of the user
	signed_id = sign_value(id)
	# Generate the activation URL
	activation_link = settings.DOMAIN_NAME + "/account/activate/?id=%s" %(signed_id)
	# Create additional context
	text    = "Thank you for registering!\nPlease follow the link below to activate your account:\n" + activation_link
	subject = "Activate your account"
	# Send the email
	send_mail(
		subject,
		text,
		settings.EMAIL_HOST_USER,
		[receiver],
		fail_silently=False,
	)

# This view is handling the account activation of a newly registered user
def activate_view(request):
	# Get the signed id string
	signed_id = request.GET.get('id')
	# Unsign it
	user_id = unsign_value(signed_id)

	# Don't like this error handling...
	# Needs to be fixed
	if user_id == -1:
		return HttpResponse('<h4>Signature has expired!</h4>')
	elif user_id == -2:
		return HttpResponse('<h4>Tampering detected!</h4>')

	user = User.objects.get(id=user_id)
	# Activate the user's account
	user.is_active=True
	user.save()
	return HttpResponse('<h4>Activation completed</h4>')

# This view is handling account changes
# It checks which form was passed by the 
# request and updates the account accordingly
def my_account_view(request):
	if request.user.is_authenticated():
		# If this is a POST request, we need to validate and save the forms
		# Then we render them with the new values pre-populated
		if request.method == 'POST':
			# The form that we have submited in the my-account page
			which_form = request.POST.get('which_form')

			#######################################################
			#  We will create some fancy "switch" functionality!  #
			#  by defining one function for each form             #
			#  Elif would probably be cleaner but this is cool!   #
			#######################################################

			# Function that handles UNA updates
			def checkUNA():
				# Create a new instance of UserForm
				user_form = UserForm(request.POST, instance=request.user)
				# We also need to post the avatar which lives in tUserProfile table
				# Create a new instance of AvatarForm
				# Notice the request.FILES. Django needs to know we are uploading a file
				user_profile_form = AvatarForm(request.POST, request.FILES, instance=request.user.tuserprofile)

				if user_form.is_valid() and user_profile_form.is_valid():
					user_form.save()
					user_profile_form.save()
					messages.success(request, 'Your account was updated successfully!')
				else:
					messages.error(request, user_form.errors)

			# Function that handles Email updates
			def checkEmail():
				# Create a new instance of the UserEmailForm form
				user_email_form = UserEmailForm(request.POST, instance=request.user)

				if user_email_form.is_valid():
					user_email_form.save()
					messages.success(request, 'Your email was updated successfully!')
				else:
					messages.error(request, user_email_form.errors)

			# Function that handles Subscription changes
			def checkSubscr():
				# Create a new instance of the SubscrForm form
				subscr_form = SubscrForm(request.POST, instance=request.user.tuserprofile)

				if subscr_form.is_valid():
					subscr_form.save()
					messages.success(request, 'Your account was updated successfully!')
				else:
					messages.error(request, subscr_form.errors)

			# Function that handles Password changes
			def checkPassword():
				# PasswordChangeForm does not inherit from ModelForm
				password_form = PasswordChangeForm(user=request.user, data=request.POST)

				if password_form.is_valid():
					user = password_form.save()
					# We need the user to stay logged in after changing the password
					update_session_auth_hash(request, user)
					messages.success(request, 'Your password was updated successfully!')
				else:
					messages.error(request, password_form.errors)

			# Function that handles Account Closure
			def checkClosure():
				account_closure_form = AccountClosureForm(request.POST, instance=request.user)

				if account_closure_form.is_valid():
					account_closure_form.save()

			# Create a dictionary that maps the form name with a function
			options = { 'UNAForm' :           checkUNA,
						'EmailForm' :         checkEmail,
						'SubscrForm' :        checkSubscr,
						'PasswordForm':       checkPassword,
						'AccountClosureForm': checkClosure
			}

			# Call the function that maps to the form name (which_form) that is passed with the request
			options[which_form]()

			return redirect('/account/my-account/')

		# If this is a GET request just render the forms, pre-populated with the existed values
		else:

			user_form            = UserForm(instance=request.user)
			user_profile_form    = AvatarForm(instance=request.user.tuserprofile)
			user_email_form      = UserEmailForm(instance=request.user)
			subscr_form          = SubscrForm(instance=request.user.tuserprofile)
			password_form        = PasswordChangeForm(user=request.user)
			account_closure_form = AccountClosureForm(instance=request.user)

		return render(request, 'accounts/my_account.html', {
			'user_form':            user_form,
			'user_profile_form':    user_profile_form,
			'user_email_form':      user_email_form,
			'subscr_form':          subscr_form,
			'password_form':        password_form,
			'account_closure_form': account_closure_form
		})
	# If the user is not authenticated redirect him/her to the home page
	else:
		return redirect('/home/')

def login_view(request):
	if request.user.is_authenticated():
		return redirect('/home/')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(username=username, password=password)

			# The default ModelBackend authentication is rejecting inactive users
			# If the user is inactive then NONE will be returned instead
			if user is not None:
				# This is just for sanity check, since if a user is inactive,
				# NONE will be returned and the code will never end up in here
				if user.is_active:
					login(request, user)
					return redirect('/home/')
			else:
				return HttpResponse('<h4>Invalid login</h4>')
		else:
			return redirect('/home/')

def logout_view(request):
	logout(request)
	return redirect('/home/')

# Function that Cryptographically signs a value
# Timestamp is also used to check expiration
def sign_value(value):
	signer = TimestampSigner()
	value  = signer.sign(value)
	return value

# Function that Cryptographically unsigns a value
def unsign_value(value):
	signer = TimestampSigner()
	try:
		value  = signer.unsign(value, max_age=timedelta(seconds=settings.EMAIL_EXPIRATION_LIMIT))
		return value
	# SignatureExpired inherites from BadSignature
	# Thus in order to catch it we have to place first
	except signing.SignatureExpired:
		return -1
	except signing.BadSignature:
		return -2
