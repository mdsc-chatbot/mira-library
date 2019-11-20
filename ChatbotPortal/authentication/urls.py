from django.urls import path
from rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_jwt.views import obtain_jwt_token

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
                    UpdateApprovedSubmissionsView,
                    UpdatePasswordView,
                    UpdateUserByAdminView)

urlpatterns = [

    # URLs that would be redirected from http://127.0.0.1:8000/chatbotportal/authentication/
    path('currentuser/', CurrentUserView.as_view(), name='auth-current-user'),

    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('register/', RegisterUsersView.as_view(), name='auth-register'),

    path('<pk>/update/', UpdateUserView.as_view(), name='auth-update'),
    path('super/<pk>/update/', UpdateUserByAdminView.as_view(), name='auth-update-by-admin'),
    path('<pk>/update/submissions/', UpdateSubmissionsView.as_view(), name='auth-update-submissions'),
    path('<pk>/update/approved_submissions/', UpdateApprovedSubmissionsView.as_view(),
         name='auth-update-approved-submissions'),

    path('<pk>/update/password/', UpdatePasswordView.as_view(), name='auth-update-password'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('delete/<pk>/', DeleteUserView.as_view(), name='auth-delete'),
    path('retrieve/', RetriveUserView.as_view(), name='auth-retrieve'),

    path('super/total/users/', TotalNumberOfUserView.as_view(), name='get-total-users'),
    path(
        'super/search/status/<str:is_active>/<str:is_reviewer>/<str:is_staff>/<str:is_superuser>/date_range/<str:search_option>/<str:start_date>/<str:end_date>/id_range/<str:start_id>/<str:end_id>/submission_range/<str:start_submission>/<str:end_submission>/<str:submission_range_option>/search_value/',
        SearchByAnythingWithFilterDateIdView.as_view(), name='search-anything-by-filter-date-id'),

    # path to get token, it uses a built in view
    path('jwt-token/', obtain_jwt_token, name='create-token'),
]
