from rest_framework import viewsets, mixins

from resource.models import Resource
from .serializers import ResourceSerializer, RetrieveResourceSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ResourceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user']

class ResourceRetrieveView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = RetrieveResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user']
