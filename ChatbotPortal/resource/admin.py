from django.contrib import admin

from .models import Resource
from .models import Tag


class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = [field.name for field in Resource._meta.get_fields()]


admin.site.register(Resource, ResourceAdmin)

# Register your models here.


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'name']


admin.site.register(Tag, TagAdmin)
