from django.contrib import admin

from .models import Resource, Tag, Category

def resource_list_display():
    # Admin cannot handle many to many relationships
    # Tag is in a many to many relationship
    list_display = [field.name for field in Resource._meta.get_fields() if field.name != 'tags' and field.name != 'category']
    list_display.append('get_tags')
    list_display.append('get_category')
    return list_display


class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = resource_list_display()
    search_fields = ['title', 'url']

    def get_tags(self, obj):
        return "\n".join([str(t.id) for t in obj.tags.all()])

    def get_category(self, obj):
        return str(obj.category.id)


admin.site.register(Resource, ResourceAdmin)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['id', 'name']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name']


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
