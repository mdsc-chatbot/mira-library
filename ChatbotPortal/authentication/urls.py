from django.urls import path

from .views import (LoginView,
                    RegisterUsersView,
                    UpdateUserView,
                    DeleteUserView,
                    RetriveUserView,
                    CurrentUserView,
                    LogoutView,
                    activate,
                    TotalNumberOfUserView,
                    SearchByAnythingWithFilterDateIdView,
                    UpdateSubmissionsView,
                    UpdatePointsView,
                    )

urlpatterns = [

    # URLs that would be redirected from http://127.0.0.1:8000/authentication/
    path('auth/currentuser/', CurrentUserView.as_view(), name='auth-current-user'),

    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('auth/register/', RegisterUsersView.as_view(), name='auth-register'),

    path('auth/<pk>/update/', UpdateUserView.as_view(), name='auth-update'),
    path('auth/<pk>/update/submissions/', UpdateSubmissionsView.as_view(), name='auth-update-submissions'),
    path('auth/<pk>/update/points/', UpdatePointsView.as_view(), name='auth-update-points'),

    path('auth/delete/<pk>/', DeleteUserView.as_view(), name='auth-delete'),
    path('auth/retrieve/', RetriveUserView.as_view(), name='auth-retrieve'),

    path('super/total/users/', TotalNumberOfUserView.as_view(), name='get-total-users'),
    path(
        'super/search/status/<str:is_active>/<str:is_reviewer>/<str:is_staff>/<str:is_superuser>/date_range/<str:search_option>/<str:start_date>/<str:end_date>/id_range/<str:start_id>/<str:end_id>/submission_range/<str:start_submission>/<str:end_submission>/search_value/',
        SearchByAnythingWithFilterDateIdView.as_view(), name='search-anything-by-filter-date-id'),
]
