
from django.http import JsonResponse, HttpResponse
from .models import Tag

# Create your views here.

def create_tags(request):
    #TODO: Add validation
    tag = Tag.objects.create(name=request.POST['name'])
    tag.save()
    #TODO: Return tag input such that tag is automatically added to input field

def fetch_tags(request):
    try:
        tag_set = Tag.objects.filter(name__contains=request.GET['name']).values('id', 'name')
        return JsonResponse(list(tag_set), safe=False)
    except:
        # Return empty http response if can't find tags
        return HttpResponse()