from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^create-tag$', views.TagCreateView.as_view(), name='create-tag'),
    re_path(r'^fetch-tags$', views.fetch_tags, name='fetch-tags'),
    re_path(r'^download-attachment/(?P<resource_id>.*)$',
            views.download_attachment, name='download-attachment'),
    re_path(r'^fetch-categories', views.fetch_categories, name='fetch-categories'),
    path('<pk>/update/', views.ResourceUpdateView.as_view()),
    path('search/', views.ResourceSearchView.as_view()),
]

router = DefaultRouter()
router.register(r'retrieve', views.ResourceRetrieveView,
                basename='retrieve-resource')
router.register(r'', views.ResourceViewSet, basename='resource')
urlpatterns.extend(router.urls)
