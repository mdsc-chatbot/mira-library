'''
urls.py:
- Urls link to Views for
1. create, fetch, get, update tags
2. fetch categories
3. download attachement
4. list, retrieve, search, update all resources and user resources (list is built in with viewset)
'''

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

from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^create-tag$', views.TagCreateView.as_view(), name='create-tag'),
    re_path(r'^fetch-tags$', views.fetch_tags, name='fetch-tags'),
    re_path(r'^fetch-tags-by-cat$', views.fetch_tags_by_cat, name='fetch-tags-by-cat'),
    re_path(r'^download-attachment/(?P<resource_id>.*)$',
            views.download_attachment, name='download-attachment'),
    re_path(r'^get-tags/(?P<resource_id>.*)$', views.gettags, name='fetch-review-tags'),
    re_path(r'^fetch-categories', views.fetch_categories, name='fetch-categories'),
    path('<pk>/update/', views.ResourceUpdateView.as_view()),
    path('<pk>/updatepartial/', views.ResourcePartialUpdate.as_view()),
    path('<pk>/updatetags/', views.TagUpdateView.as_view()),
    path('search/', views.ResourceSearchView.as_view()),
]

router = DefaultRouter()
router.register(r'retrieve', views.ResourceRetrieveView,
                basename='retrieve-resource')
router.register(r'', views.ResourceViewSet, basename='resource')
urlpatterns.extend(router.urls)
