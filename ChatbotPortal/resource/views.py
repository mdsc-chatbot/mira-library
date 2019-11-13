from rest_framework import permissions, generics, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .serializers import ResourceSerializer, RetrieveResourceSerializer, ResourceUpdateSerializer
from .models import Resource, Tag
import json
import mimetypes

def create_tags(request):
    form_data = json.loads(request.body.decode('utf-8'))

    # Validation
    # Name of tag must be unique (case insensitive)
    if (Tag.objects.filter(name__iexact=form_data['name']).count() != 0):
        return JsonResponse({
            'name' : 'Tag already exists.'
        }, status=400)

    # Saving it
    tag = Tag.objects.create(name=form_data['name'])
    tag.save()

    # Return tag so that frontend can dynamically add it to the dropdown
    return JsonResponse({
        'id' : tag.id,
        'name' : tag.name,
    })


def fetch_tags(request):
    try:
        tag_set = Tag.objects.filter(
            name__contains=request.GET['name']).values('id', 'name')
        return JsonResponse(list(tag_set), safe=False)
    except:
        # Return empty http response if can't find tags
        return HttpResponse()

# Downloads request attachment
def download_attachment(request, resource_id):
    resource = Resource.objects.get(pk=int(resource_id))

    content_type = mimetypes.guess_type(resource.attachment.name)
    response = HttpResponse(
        resource.attachment.file.read(), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        resource.attachment.name.rsplit('/', 1)[-1])

    return response


class ResourceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances (list, create, retrieve, delete, update, partial_update, destroy).
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user']


class ResourceRetrieveView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RetrieveResourceSerializer
    queryset = Resource.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by_user']


class ResourceUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResourceUpdateSerializer
    queryset = Resource.objects.all()
