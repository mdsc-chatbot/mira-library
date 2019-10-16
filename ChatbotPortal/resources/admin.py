from django.contrib import admin
from .models import Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'name']

admin.site.register(Tag, TagAdmin)