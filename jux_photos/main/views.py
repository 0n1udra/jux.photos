from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'homepage.html', {})

def handler_404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler_404.html', None, None, 404)
