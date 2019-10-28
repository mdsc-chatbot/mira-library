from rest_framework.routers import DefaultRouter

from .views import ResourceViewSet, ResourceRetrieveView

router = DefaultRouter()
router.register(r'retrieve', ResourceRetrieveView, basename='retrieve-resource')
router.register(r'', ResourceViewSet, basename='resource')

urlpatterns = router.urls