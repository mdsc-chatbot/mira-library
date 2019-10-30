import json, mimetypes
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Resource, Tag


# Create your views here.


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
    response = HttpResponse(resource.attachment.file.read(), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(resource.attachment.name.rsplit('/', 1)[-1])

    return response
    
def fetch_tags_by_id(request):
    try:
        idlist = []
        print("yes", request.GET['ids'])
        for idFind in request.GET['ids']:
            print(idFind)
            tag = Tag.objects.filter(id = idFind)
            idlist.append(tag)
        return idlist
    except:
        # Return empty http response if can't find tags
        return []

def fetch_all_tags(request):
    try:
        tag_set = Tag.objects.filter(approved=False)
        return JsonResponse(list(tag_set), safe=False)
    except:
        # Return empty http response if can't find tags
        return None
