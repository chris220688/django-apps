# Django imports
from django.http import Http404
from django.shortcuts import render

# Local Django imports
from .models import tHomeContent


def index(request):
    """ Handle a GET request to /index.

        Args:
            request: A GET HttpRequest to /index

        Returns:
            An HttpResponse object with the home content
    """

    template = 'home/index.html'

    all_content = tHomeContent.objects.all()
    context = {'all_content': all_content,}

    return render(request, template, context)