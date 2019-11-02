from django.urls import path

from .views import (LoginView,
                    RegisterUsersView,
                    UpdateUserView,
                    DeleteUserView,
                    RetriveUserView,
                    CurrentUserView,
                    LogoutView,
                    activate,
                    AllUsersView,
                    SearchByDateRangeView,
                    SearchByIdRangeView,
                    SearchByAnythingView,
                    SearchFilterUserView,
                    TotalNumberOfUserView,
                    )

urlpatterns = [
    # path('current_user/', current_user, name='current_user'),
    # path('users/', UserCreateList.as_view(), name='user_create_list'),
    # path('<pk>/update/', UserUpdateList.as_view(), name='user_update'),

    # URLs that would be redirected from http://127.0.0.1:8000/authentication/
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/register/', RegisterUsersView.as_view(), name='auth-register'),
    path('auth/<pk>/update/', UpdateUserView.as_view(), name='auth-update'),
    path('auth/delete/<pk>/', DeleteUserView.as_view(), name='auth-delete'),
    path('auth/retrieve/', RetriveUserView.as_view(), name='auth-retrieve'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/currentuser/', CurrentUserView.as_view(), name='auth-current-user'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('super/search/alluser/', AllUsersView.as_view(), name='search-alluser'),
    path('super/search/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/', SearchByDateRangeView.as_view(), name='search-by-date-range'),
    path('super/search/id_range/<int:start_id>/<int:end_id>/', SearchByIdRangeView.as_view(), name='search-by-id-range'),
    path('super/search/by_anything/', SearchByAnythingView.as_view(), name='search-by-anything'),
    path('super/search/filter/<str:filter_by>/<str:filter_value>/', SearchFilterUserView.as_view(), name='search-filter-user'),
    path('super/total/users/', TotalNumberOfUserView.as_view(), name='get-total-user'),
]
