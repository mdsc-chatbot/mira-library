from rest_framework.routers import DefaultRouter

from .views import ResourceViewSet, ResourceRetrieveView, ResourceUpdateView
from django.urls import path


router = DefaultRouter()
router.register(r'retrieve', ResourceRetrieveView, basename='retrieve-resource')
router.register(r'', ResourceViewSet, basename='resource')

urlpatterns = router.urls
urlpatterns.append(path('<pk>/update/', ResourceUpdateView.as_view()))