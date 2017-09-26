from django.conf.urls import url
import about.views

urlpatterns = [
	# /about/
    url(r'^$', about.views.about, name='about'),
]