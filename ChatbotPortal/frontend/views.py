from django.shortcuts import render

# Create your views here.
def index(request, resourceID=None):
    return render(request, 'webpack/index.html')

def resources(request, path):
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

    return render(request, 'webpack/' + path, content_type=content_type)