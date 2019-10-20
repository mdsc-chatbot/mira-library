from django.urls import path, include
from . import views
from rest_framework import routers
from .views import ProfileViewSet

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]