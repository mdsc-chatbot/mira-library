from django.urls import path, re_path
from . import views
urlpatterns = [
    re_path(r'^create-tag$', views.create_tags, name='create-tag'),
    re_path(r'^fetch-tags$', views.fetch_tags, name='fetch-tags'),
    re_path(r'^download-attachment/(?P<resource_id>.*)$', views.download_attachment, name='download-attachment')
    re_path(r'^fetch-all-tags$', views.fetch_all_tags, name='fetch-all-tags'),
    re_path(r'^fetch-tags-by-id$', views.fetch_tags_by_id, name='fetch-tags-by-id'),
]