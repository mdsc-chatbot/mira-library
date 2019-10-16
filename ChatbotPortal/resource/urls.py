from django.urls import path, re_path
from . import views
urlpatterns = [
    re_path(r'^create-tag$', views.create_tags, name='create-tag'),
    re_path(r'^fetch-tags$', views.fetch_tags, name='fetch-tags'),
]