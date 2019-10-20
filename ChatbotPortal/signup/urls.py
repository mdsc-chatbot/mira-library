from django.urls import path
from .views import current_user, UserCreateList, UserUpdateList

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserCreateList.as_view()),
    path('<pk>/update/', UserUpdateList.as_view())
]