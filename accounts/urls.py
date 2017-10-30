# Django imports
from django.conf.urls import url
from django.contrib.auth import views as auth_views

# Local Django imports
import accounts.views

urlpatterns = [
    # /account/register/
    url(r'^register/$', accounts.views.register_view, name='register_view'),
    # /account/login/
    url(r'^login/$', accounts.views.login_view, name='login_view'),
    # /account/logout/
    url(r'^logout/$', accounts.views.logout_view, name='logout_view'),
    # /account/my-ccount/
    url(r'^my-account/$', accounts.views.my_account_view, name='my_account_view'),
    # /account/activate/
    url(r'^activate/', accounts.views.activate_view, name='activate_view'),
    # From django.contrib.auth.urls. Used to reset a password.
    # /account/password_reset/
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # /account/password_reset/done/
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # /account/reset/
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    # /account/reset/done/
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]