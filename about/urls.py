# Django imports
from django.conf.urls import url

# Local Django imports
import about.views


urlpatterns = [
    # /about/
    url(r'^$', about.views.about, name='about'),
]