'''
views.py:
- Django views for 
1. create tag, fetch tag, get tags, Tag Create View, Tag Update View
2. fetch categories
3. download attachment
4. Resource View (user resources only), Resource Retrieve View, Resource Update View, Resource Search View
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

from rest_framework import permissions, generics, viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .serializers import ResourceSerializer, RetrieveResourceSerializer, ResourceUpdateSerializer, TagSerializer, TagUpdateSerializer
from .models import Resource, Tag, Category, ResourceFlags
import json
import mimetypes
from datetime import datetime
from django.db.models import Q


def create_tags(request):
    form_data = json.loads(request.body.decode('utf-8'))

    # Validation
    # Name of tag must be unique (case insensitive)
    if (Tag.objects.filter(name__iexact=form_data['name']).count() != 0):
        return JsonResponse({
            'name': 'Tag already exists.'
        }, status=400)

    # Saving it
    tag = Tag.objects.create(name=form_data['name'],tag_category = form_data['tag_category'])
    tag.save()

    # Return tag so that frontend can dynamically add it to the dropdown
    return JsonResponse({
        'id': tag.id,
        'name': tag.name,
        'tag_category': tag.tag_category
    })


def fetch_tags(request):
    try:
        tag_set = Tag.objects.filter(
            name__icontains=request.GET['name'], approved=True).values('id', 'name')
        return JsonResponse(list(tag_set), safe=False)
    except:
        # Return empty http response if can't find tags
        return HttpResponse()

def fetch_tags_by_cat(request):
    try:
        tag_set = Tag.objects.filter(
            name__icontains=request.GET['name'], tag_category__contains=request.GET['tag_category'], approved=True).values('id', 'name')
        return JsonResponse(list(tag_set), safe=False)
    except:
        # Return empty http response if can't find tags
        return HttpResponse()

def fetch_categories(request):
    category_set = Category.objects.all().values()
    return JsonResponse(list(category_set), safe=False)

def gettags(request, resource_id):
    resource = Resource.objects.get(pk=int(resource_id))
    tags = resource.tags.all()
    tagSent = []
    for item in tags:
        print(item)
        tag_set = {'id':item.id, 'name':item.name, 'approved':item.approved, 'tag_category':item.tag_category}
        tagSent.append(tag_set)

    return JsonResponse(tagSent, safe=False)

def getAllPTags(request):
    resources = Resource.objects.all()
    tagSent = []

    for resource in resources:
        tags = resource.tags.exclude(approved__exact = 1) 
        for item in tags:
            tag_set = {'resourceId':resource.id}
            if tag_set not in tagSent:
                tagSent.append(tag_set)

    return JsonResponse(tagSent, safe=False)

# Downloads request attachment
def download_attachment(request, resource_id):
    resource = Resource.objects.get(pk=int(resource_id))

    content_type = mimetypes.guess_type(resource.attachment.name)
    response = HttpResponse(
        resource.attachment.file.read(), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        resource.attachment.name.rsplit('/', 1)[-1])

    return response

def flag_resource(request):
    data = json.loads(request.body)
    resource_id = data['resource_id']
    flag_id = data['flag_id']

    #get flag by id
    flag = ResourceFlags.objects.get(pk=int(flag_id))

    # add the flag to the resource
    resource = Resource.objects.get(pk=int(resource_id))
    resource.flags.add(flag)
    resource.save()

    # Return empty response
    return HttpResponse()


class ResourceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user_pk']


class ResourceRetrieveView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RetrieveResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user_pk']


class ResourceUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResourceUpdateSerializer
    queryset = Resource.objects.all()

class TagUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagUpdateSerializer
    queryset = Tag.objects.all()

class ResourceSearchView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResourceSerializer
    queryset = Resource.objects.filter(
        (Q(review_status="approved") & Q(review_status_2="approved")) |
        (Q(review_status_2_2="approved") & Q(review_status_1_1="approved")) |
        (Q(review_status="approved") & Q(review_status_2_2="approved")) | 
        (Q(review_status="approved") & Q(review_status_1_1="approved")) | 
        (Q(review_status_2="approved") & Q(review_status_2_2="approved")) | 
        (Q(review_status_2="approved") & Q(review_status_1_1="approved")) | 
        Q(review_status_3="approved")
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'url']
    

class TagCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

class ResourcePartialUpdate(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    def put(self, request, *args, **kwargs):
        if 'assigned_reviewer' in request.data:
            request.data['reviewer_assigned_at'] = datetime.now()
        if 'assigned_reviewer_2' in request.data:
            request.data['reviewer_2_assigned_at'] = datetime.now()
        if 'review_status' in request.data:
            request.data['reviewer_updated_at'] = datetime.now()
        if 'review_status_2' in request.data:
            request.data['reviewer_2_updated_at'] = datetime.now()

        if 'review_status_1_1' in request.data:
            request.data['reviewer_1_1_updated_at'] = datetime.now()
        if 'review_status_2_2' in request.data:
            request.data['reviewer_2_2_updated_at'] = datetime.now()
        if 'assigned_reviewer_1_1' in request.data:
            request.data['reviewer_1_1_assigned_at'] = datetime.now()
        if 'assigned_reviewer_2_2' in request.data:
            request.data['reviewer_2_2_assigned_at'] = datetime.now()

        return self.partial_update(request, *args, **kwargs)