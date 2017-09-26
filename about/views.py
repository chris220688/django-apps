from django.shortcuts import render

def about(request):
    template = 'about/about.html'
    return render(request, template, {})