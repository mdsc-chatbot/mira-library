'''
admin.py:
- register admin view for resource, tags and categories objects
'''

__author__ = "Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen"
__copyright__ = "Copyright (c) 2019 BOLDDUC LABORATORY"
__credits__ = ["Apu Islam", "Henry Lo", "Jacy Mark", "Ritvik Khanna", "Yeva Nguyen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "BOLDDUC LABORATORY"

#  MIT License
#
#  Copyright (c) 2019 BOLDDUC LABORATORY
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
    list_display = ['id', 'name', 'approved']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name']


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
