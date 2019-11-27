"""urls.py: The urls associated with authentication app related tasks are defined here."""

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
