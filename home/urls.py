from django.conf.urls import url
from . import views

urlpatterns = [
	#/index/
    url(r'^$', views.index, name='index'),
]