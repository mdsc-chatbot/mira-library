__author__ = "Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen"
__copyright__ = "Copyright (c) 2019 BOLDDUC LABORATORY"
__credits__ = ["Apu Islam", "Henry Lo", "Jacy Mark", "Ritvik Khanna", "Yeva Nguyen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "BOLDDUC LABORATORY"

#  MIT License
#
#  Copyright (c) 2019 BOLDDUC LABORATORY
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
    elif path.endswith('.woff'):
        content_type = 'application/font-woff'
    elif path.endswith('.ttf'):
        content_type = 'application/font-ttf'
    elif path.endswith('.svg'):
        content_type = 'image/svg+xml' 

    file = open(path_string, "rb")
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