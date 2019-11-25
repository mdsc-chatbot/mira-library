from django.urls import path
from .views import ResourceView, TagView, CategoryView, DetailedResourceView, DetailedResourceAdminView, HomepageResourceView

urlpatterns = [
    # path('current_user/', current_user, name='current_user'),
    # path('users/', UserCreateList.as_view(), name='user_create_list'),
    # path('<pk>/update/', UserUpdateList.as_view(), name='user_update'),

    # URLs that would be redirected from http://127.0.0.1:8000/chatbotportal/authentication/
    path('homepage-resources', HomepageResourceView.as_view(), name='homepage_resources'),
    path('resources', ResourceView.as_view(), name='resources'),
    path('tags', TagView.as_view(), name='tags'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('retrieve/<int:pk>', DetailedResourceView.as_view(), name='detailed_resource'),
    path('retrieve-admin/<int:pk>', DetailedResourceAdminView.as_view(), name='detailed_resource')
]