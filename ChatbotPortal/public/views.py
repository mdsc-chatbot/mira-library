from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from resource.models import Resource, Tag
from resource.serializers import RetrieveResourceSerializer
from .serializers import ResourceSerializer, TagSerializer, RetrievePublicResourceSerializer


class StandardResultSetPagination(PageNumberPagination):
    page_size = 100


class ResourceView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        # Taken from PR #164
        queryset = Resource.objects.filter(review_status="approved")

        # Search parameters is matched between two fields currently:
        #   - title
        #   - website summary
        search_param = self.request.query_params.get('search')
        if (search_param != None and search_param != ""):
            matching_titles = Resource.objects.filter(title__icontains=search_param)
            matching_url = Resource.objects.filter(url__icontains=search_param)
            #TODO Uncomment this when summary comes back? (if it comes baCk)
            # matching_summary = Resource.objects.filter(website_summary_metadata__icontains=search_param)
            # queryset = queryset.intersection(matching_titles.union(matching_url, matching_summary))
            queryset = queryset.intersection(matching_titles.union(matching_url))

        # Filter resources by tags
        tag_param = self.request.query_params.get('tags')
        if (tag_param != None and tag_param != ""):

            # Assumes that tags are separated via commas in a string
            tag_list = tag_param.split(',')
            queryset = queryset.filter(tags__id__in=tag_list)

        # Sort query
        # 0, 3 : Recency (desc, asc)
        # 1, 4 : Popularity (desc, asc)
        # 2, 5 : Rating (desc, asc)
        # Reference on how to do complex sorting: https://stackoverflow.com/questions/19623311/how-to-order-django-queryset-by-a-specified-match-and-then-default-to-the-origin
        sort_param = int(self.request.query_params.get('sort'))
        if (sort_param == None or sort_param == "" or sort_param == 0 or sort_param == 3 or sort_param == 1 or sort_param == 4):
            # By default, popularity is also recency
            # TODO: Figure out how to do popularity sort...
            if (sort_param == 0):
                queryset = queryset.order_by('-timestamp')
            else:
                queryset = queryset.order_by('timestamp')
        elif (sort_param == 2 or sort_param == 5):
            if (sort_param == 2):
                queryset = queryset.order_by('-rating')
            else:
                queryset = queryset.order_by('rating')

        return queryset

class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Only approved tags?? Waiting for client confirmation
        # TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.all()

class DetailedResourceView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}

class DetailedResourceAdminView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrieveResourceSerializer
    permissions_classes = {permissions.IsAdminUser}
