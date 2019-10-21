from django.urls import path
from .views import current_user, UserCreateList, UserUpdateList

urlpatterns = [
    path('current_user/', current_user, name='current_user'),
    path('users/', UserCreateList.as_view(), name='user_create_list'),
    path('<pk>/update/', UserUpdateList.as_view(), name='user_update')
]