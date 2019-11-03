from django.shortcuts import render, redirect
import os, re
from django.http import HttpResponse

# Create your views here.
def index(request, path, resourceID=None):
    return render(request, 'webpack/index.html')

def redirect_index(request):
    return redirect('/chatbotportal/app')

def resources(request, path):
    # We can no longer rely on django templates
    # The code in webpack will conflict
    path_string = os.path.join(os.path.dirname(__file__), 'react', 'webpack')
    for path_item in path.split("/"):
        path_string = os.path.join(path_string, path_item)

    # We may have to handle more than these data types
    #TODO: Find out a dynamic way of figuring out content type
    content_type = 'text/html'
    if path.endswith('.js'):
        content_type = 'text/javascript'
    elif path.endswith('.css'):
        content_type = 'text/css'
    elif path.endswith('.png'):
        content_type = 'image/png'
    elif path.endswith('.woff2'):
        content_type = 'application/font-woff2'

    file = open(path_string, encoding="utf-8")
    return HttpResponse(file.read(), content_type=content_type)

def review(request, path):
    path_string = os.path.join(os.path.dirname(__file__), 'react', 'webpack')
    for path_item in path.split("/"):
        path_string = os.path.join(path_string, path_item)
    
    content_type = 'text/html'
    if path.endswith('.js'):
        content_type = 'text/javascript'

    file = open(path_string, encoding="utf-8")
    return HttpResponse(file.read(), content_type=content_type)