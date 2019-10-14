from django.urls import path, re_path
from . import views
urlpatterns = [
    re_path(r'^fetch-tags$', views.fetch_tags, name='resources'),
]