from rest_framework import generics

from resource.models import Resource, Tag
from .serializers import ResourceSerializer, TagSerializer


class ResourceView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = ResourceSerializer
    def get_queryset(self):
        #TODO: Filter
        return Resource.objects.all()

class TagView(generics.ListAPIView):

    serializer_class = TagSerializer

    def get_queryset(self):
        #TODO: Filter
        return Tag.objects.all()