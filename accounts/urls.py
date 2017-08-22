from django.conf.urls import url
import accounts.views

urlpatterns = [
	#/account/register/
    url(r'^register/$',   accounts.views.register_view,  name='register_view'),
    #/account/login/
    url(r'^login/$',      accounts.views.login_view,     name='login_view'),
    #/account/logout/
    url(r'^logout/$',     accounts.views.logout_view,     name='logout_view'),
    #/account/my_account/
    url(r'^my-account/$', accounts.views.my_account_view, name='my_account_view'),
	# /account/activation/
	url(r'^activate/',  accounts.views.activate_view,   name='activate_view'),
]