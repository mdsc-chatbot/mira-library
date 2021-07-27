'''
views.py

List views for homepage resources, resources, tags, categories
Retrive views for user resource and admin resource
Pagination views
Retrive views based on resource sorting
'''
__author__ = "Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen"
__copyright__ = "Copyright (c) 2019 BOLDDUC LABORATORY"
__credits__ = ["Apu Islam", "Henry Lo", "Jacy Mark", "Ritvik Khanna", "Yeva Nguyen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "BOLDDUC LABORATORY"

#  MIT License
#
#  Copyright (c) 2019 BOLDDUC LABORATORY
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from resource.models import Resource, Tag, Category
from resource.serializers import RetrieveResourceSerializer
from .serializers import ResourceSerializer, TagSerializer, CategorySerializer, RetrievePublicResourceSerializer


class StandardResultSetPagination(PageNumberPagination):
    page_size = 100

class HomepageResultSetPagination(PageNumberPagination):
    page_size = 4


def ResourceViewQuerySet(query_params):
    # Taken from PR #164
    queryset = Resource.objects.filter(review_status="approved")

    # Search parameters is matched between four fields currently:
    #   - title
    #   - url
    #   - website summary
    #   - definition
    search_param = query_params.get('search')
    if (search_param != None and search_param != ""):
        matching_titles = Resource.objects.filter(title__icontains=search_param)
        matching_url = Resource.objects.filter(url__icontains=search_param)
        matching_summary = Resource.objects.filter(website_summary_metadata__icontains=search_param)
        matching_definition = Resource.objects.filter(definition__icontains=search_param)
        queryset = queryset.filter(id__in=[resource.id for resource in matching_titles.union(matching_url, matching_summary, matching_definition)])

    # Filter resources by categories
    category_param = query_params.get('categories')
    if (category_param != None and category_param != ""):

        # Assumes that tags are separated via commas in a string
        category_list = category_param.split(',')
        queryset = queryset.filter(category__id__in=category_list)

    # Filter resources by tags
    tag_param = query_params.get('tags')
    if (tag_param != None and tag_param != ""):

        # Assumes that tags are separated via commas in a string
        tag_list = tag_param.split(',')
        queryset = queryset.filter(tags__id__in=tag_list)

    # Sort query
    # 0, 3 : Recency (desc, asc)
    # 1, 4 : Popularity (desc, asc)
    # 2, 5 : Rating (desc, asc)
    # Reference on how to do complex sorting: https://stackoverflow.com/questions/19623311/how-to-order-django-queryset-by-a-specified-match-and-then-default-to-the-origin
    sort_param = int(query_params.get('sort'))
    if (sort_param == None or sort_param == "" or sort_param == 0 or sort_param == 3):
        # By default, popularity is also recency
        if (sort_param == 0):
            queryset = queryset.order_by('-timestamp')
        else:
            queryset = queryset.order_by('timestamp')
    elif (sort_param == 1 or sort_param == 4):
        if (sort_param == 1):
            queryset = queryset.order_by('-public_view_count')
        else:
            queryset = queryset.order_by('public_view_count')
    elif (sort_param == 2 or sort_param == 5):
        if (sort_param == 2):
            queryset = queryset.order_by('-rating')
        else:
            queryset = queryset.order_by('rating')

    return queryset


class HomepageResourceView(generics.ListAPIView):
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = HomepageResultSetPagination

    def get_queryset(self):
        return ResourceViewQuerySet(self.request.query_params)


class ResourceView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        return ResourceViewQuerySet(self.request.query_params)


class TagView(generics.ListAPIView):
    serializer_class = TagSerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Only approved tags?? Waiting for client confirmation
        # TODO: Tag sorting? (Sort desc by most used)
        return Tag.objects.filter(approved=True).order_by('name')


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = {permissions.AllowAny}

    def get_queryset(self):
        # TODO: Category sorting? (Sort desc by most used)
        return Category.objects.all()


class DetailedResourceView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrievePublicResourceSerializer
    permission_classes = {permissions.AllowAny}

    # Override generics.RetrieveAPIView here to insert view count update
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.public_view_count += 1
        instance.save()
        return self.retrieve(request, *args, **kwargs)


class DetailedResourceAdminView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = RetrieveResourceSerializer
    permissions_classes = {permissions.IsAdminUser}
