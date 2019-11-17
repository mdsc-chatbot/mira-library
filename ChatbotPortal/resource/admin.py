from django.contrib import admin

from .models import Resource
from .models import Tag

def resource_list_display():
    # Admin cannot handle many to many relationships
    # Tag is in a many to many relationship
    list_display = [field.name for field in Resource._meta.get_fields() if field.name != 'tags']
    list_display.append('get_tags')
    return list_display

class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = resource_list_display()
    search_fields = ['title', 'url']

    def get_tags(self, obj):
        return "\n".join([str(t.id) for t in obj.tags.all()])


admin.site.register(Resource, ResourceAdmin)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'name']


admin.site.register(Tag, TagAdmin)
