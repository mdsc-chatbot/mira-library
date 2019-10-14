from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from .models import Tags

# Create your views here.
#TODO: Add way to create tags...
def fetch_tags(request):
    tag_set = None
    try:
        tag_set = Tags.objects.get(name__contains=request.GET['name'])
    except:
        # Return empty http response if can't find tags
        return HttpResponse()
    json_tags = serializers.serialize('json', tag_set)
    return JsonResponse(json_tags)