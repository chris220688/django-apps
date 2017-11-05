# Django imports
from django.conf.urls import url

# Local Django imports
import home.views


urlpatterns = [
    # /index/
    url(r'^$', home.views.index, name='index'),
]