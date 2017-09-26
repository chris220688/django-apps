from django.conf.urls import url
import home.views

urlpatterns = [
	#/index/
    url(r'^$', home.views.index, name='index'),
]