from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from resource.models import Resource, Tag
from .serializers import ResourceSerializer, TagSerializer

class StandardResultSetPagination(PageNumberPagination):
    page_size = 100

class ResourceView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = ResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        #TODO We should NOT get all resources, only approved ones.
        queryset = None

        # Search parameters is matched between two fields currently:
        #   - title
        #   - website summary
        search_param = self.request.query_params.get('search')
        if (search_param != None and search_param != ""):
            matching_titles = Resource.objects.filter(title__icontains=search_param)
            matching_summary = Resource.objects.filter(website_summary_metadata__icontains=search_param)
            queryset = matching_titles.union(matching_summary)
        else:
            queryset = Resource.objects.all()

        # Filter resources by tags
        tag_param = self.request.query_params.get('tags')
        if (tag_param != None and tag_param != ""):

            # Assumes that tags are separated via commas in a string
            tag_list = tag_param.split(',')
            queryset = queryset.filter(tags__id__in=tag_list)

        return queryset

class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        #TODO: Only approved tags?? Waiting for client confirmation
        #TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.all()