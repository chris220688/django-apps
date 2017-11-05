# Django imports
from django.shortcuts import render


def about(request):
    """ Handle a GET request to /about.

        Args:
            request: A GET HttpRequest to /about

        Returns:
            An HttpResponse object with the about content
    """

    template = 'about/about.html'

    return render(request, template, {})