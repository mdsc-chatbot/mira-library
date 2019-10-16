from django.contrib import admin

from .models import Resource

class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = [field.name for field in Resource._meta.get_fields()]

admin.site.register(Resource, ResourceAdmin)