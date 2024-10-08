'''
urls.py
url link to views of:
- homepage resources, resources, tags, categories
- retrieve resource detail for user and admin
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

from django.urls import path
from .views import ResourceView, get_tag_group_stats, TagView, CategoryView, DetailedResourceView, DetailedResourceAdminView, HomepageResourceView, IndexResourceEntityView, VerifyApprovedResourcesView, ResourceCountAndFilterView, ResourceStatsView, ResourceByIntentEntityView_new, AddViewOfResourceView, ResourceByIntentEntityView_new_new, EmotionTest, AllTagView, add_tag_alias, GetAliasByTagView, remove_tag_alias

urlpatterns = [
    # path('current_user/', current_user, name='current_user'),
    # path('users/', UserCreateList.as_view(), name='user_create_list'),
    # path('<pk>/update/', UserUpdateList.as_view(), name='user_update'),

    # URLs that would be redirected from '/chatbotportal/authentication/'
    path('homepage-resources', HomepageResourceView.as_view(), name='homepage_resources'),
    path('resources', ResourceView.as_view(), name='resources'),
    path('resources-by-intent-entity-new-new', ResourceByIntentEntityView_new.as_view(), name='resource_by_intent_entity'),
    path('resources-by-intent-entity-new', ResourceByIntentEntityView_new_new.as_view(), name='resource_by_intent_entity'),
    path('resources-stats', ResourceStatsView.as_view(), name='resources-stats'),
    path('resource-stats', get_tag_group_stats, name='resource-stats'),
    path('resource-count-and-filter', ResourceCountAndFilterView.as_view(), name='count_resource'),
    path('index-resources', IndexResourceEntityView.as_view(), name='index_resource'),
    path('verify-resources', VerifyApprovedResourcesView.as_view(), name='verify_resource'),
    path('add-view-of-resource', AddViewOfResourceView.as_view(), name='add_view_resource'),
    path('emotion-test', EmotionTest.as_view(), name='Emotion_Test'),
    path('tags', TagView.as_view(), name='tags'),
    path('alltags', AllTagView.as_view(), name='alltags'),
    path("add-tag-alias", add_tag_alias, name='add-tag-alias'),
    path("get-alias-by-tag", GetAliasByTagView.as_view(), name='get-alias-by-tag'),
    path("remove-tag-alias", remove_tag_alias, name='remove-tag-alias'),
    #path('get-relations-by-tag', get_relations_by_tag, name='get-relations-by-tag'),
    #path('add-tag-relation', add_tag_relation, name='add-tag-relation'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('retrieve/<int:pk>', DetailedResourceView.as_view(), name='detailed_resource'),
    path('retrieve-admin/<int:pk>', DetailedResourceAdminView.as_view(), name='detailed_resource')
]