from django.urls import path
from .views import ResourceView, TagView

urlpatterns = [
    # path('current_user/', current_user, name='current_user'),
    # path('users/', UserCreateList.as_view(), name='user_create_list'),
    # path('<pk>/update/', UserUpdateList.as_view(), name='user_update'),

    # URLs that would be redirected from http://127.0.0.1:8000/authentication/
    path('resources', ResourceView.as_view(), name='resources'),
    path('tags', TagView.as_view(), name='tags'),
]