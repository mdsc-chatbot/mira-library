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
                    RangeOfUsersView,
                    SearchByAnythingWithFilterDateIdView,
                    UpdateSubmissionsView,
                    UpdatePointsView,
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

    path('auth/<pk>/update/submissions/', UpdateSubmissionsView.as_view(), name='auth-update'),
    path('auth/<pk>/update/points/', UpdatePointsView.as_view(), name='auth-update'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('super/search/alluser/', AllUsersView.as_view(), name='search-alluser'),
    path('super/search/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/', SearchByDateRangeView.as_view(), name='search-by-date-range'),
    path('super/search/id_range/<int:start_id>/<int:end_id>/', SearchByIdRangeView.as_view(), name='search-by-id-range'),
    path('super/search/by_anything/', SearchByAnythingView.as_view(), name='search-by-anything'),
    path('super/search/filter/<str:filter_by>/<str:filter_value>/', SearchFilterUserView.as_view(), name='search-filter-user'),
    path('super/total/users/', TotalNumberOfUserView.as_view(), name='get-total-user'),
    path('super/rows/<int:start_row>/<int:end_row>/', RangeOfUsersView.as_view(), name='get-rows'),

    # path('super/search/filter/<str:filter_by>/<str:filter_value>/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/id_range/<str:start_id>/<str:end_id>/search_value/', SearchByAnythingWithFilterDateIdView.as_view(), name='search-anything-by-filter-date-id'),

    path('super/search/status/<str:is_active>/<str:is_reviewer>/<str:is_staff>/<str:is_superuser>/date_range/<str:search_option>/<str:start_date>/<str:end_date>/id_range/<str:start_id>/<str:end_id>/submission_range/<str:start_submission>/<str:end_submission>/search_value/', SearchByAnythingWithFilterDateIdView.as_view(), name='search-anything-by-filter-date-id'),
]
