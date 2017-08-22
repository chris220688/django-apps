from django.http import Http404
from django.shortcuts import render
from .models import tHomeContent

def index(request):
	all_content = tHomeContent.objects.all()
	template = 'home/index.html'
	context = {
		'all_content': all_content,
	}
	return render(request, template, context)