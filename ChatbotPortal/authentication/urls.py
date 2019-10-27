from django.conf.urls import url
from django.urls import path

from .views import LoginView, RegisterUsersView, UpdateUserView, DeleteUserView, RetriveUserView, CurrentUserView, LogoutView, activate

urlpatterns = [
    # path('current_user/', current_user, name='current_user'),
    # path('users/', UserCreateList.as_view(), name='user_create_list'),
    # path('<pk>/update/', UserUpdateList.as_view(), name='user_update'),

    # URLs that would be redirected from http://127.0.0.1:8000/authentication/
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterUsersView.as_view(), name='auth-register'),
    path(r'auth/<pk>/update/', UpdateUserView.as_view(), name='auth-update'),
    path(r'auth/delete/<pk>/', DeleteUserView.as_view(), name='auth-delete'),
    path('auth/retrieve/', RetriveUserView.as_view(), name='auth-retrieve'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/currentuser/', CurrentUserView.as_view(), name='auth-current-user'),

    path(r'activate/<uidb64>/<token>/', activate, name='activate'),
]
