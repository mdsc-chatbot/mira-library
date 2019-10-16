from django.contrib import admin
from .models import Tags

# Register your models here.
class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display = ['id', 'name']

admin.site.register(Tags, TagsAdmin)