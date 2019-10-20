import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Tag


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
