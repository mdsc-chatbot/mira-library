from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_auth.views import PasswordResetView, PasswordResetConfirmView

from ..views import (LoginView,
                     RegisterUsersView,
                     UpdateUserView,
                     DeleteUserView,
                     RetriveUserView,
                     CurrentUserView,
                     LogoutView,
                     activate,
                     UpdateSubmissionsView, UpdatePointsView, TotalNumberOfUserView,
                     SearchByAnythingWithFilterDateIdView, UpdatePasswordView)


class TestUrls(SimpleTestCase):
    """
    Tests the urls redirected from http://127.0.0.1:8000/signup/
    """

    def test_currentuser_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/auth/currentuser/ url.
        :return: None
        """
        url = reverse('auth-current-user')
        self.assertEquals(resolve(url).func.view_class, CurrentUserView)

    def test_login_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/login url.
        :return: None
        """
        url = reverse('auth-login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/auth/logout/ url.
        :return: None
        """
        url = reverse('auth-logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_activation_url(self):
        """
        Tests the Tests the activate/<uidb64>/<token>/ url.
        :return: None
        """
        url = reverse('activate', args=['some-pk', 'some-token'])
        self.assertEquals(resolve(url).func, activate)

    def test_register_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/register url.
        :return: None
        """
        url = reverse('auth-register')
        self.assertEquals(resolve(url).func.view_class, RegisterUsersView)

    def test_update_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/<pk>/update/ url.
        :return: None
        """
        url = reverse('auth-update', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdateUserView)

    def test_update_submissions_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/<pk>/update/submissions/ url.
        :return: None
        """
        url = reverse('auth-update-submissions', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdateSubmissionsView)

    def test_update_points_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/<pk>/update/points url.
        :return: None
        """
        url = reverse('auth-update-points', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdatePointsView)

    def test_update_password_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/<pk>/update/password/ url.
        :return: None
        """
        url = reverse('auth-update-password', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdatePasswordView)

    def test_PasswordResetView_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/password/reset/ url.
        :return: None
        """
        url = reverse('password-reset')
        self.assertEquals(resolve(url).func.view_class, PasswordResetView)

    def test_PasswordResetConfirmView_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/password/reset/confirm/<uidb64>/<token>/ url.
        :return: None
        """
        url = reverse('password_reset_confirm', args=['MO', 'adsa654sdft4532esdhfg'])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_delete_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/auth/delete/<pk> url.
        :return: None
        """
        url = reverse('auth-delete', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, DeleteUserView)

    def test_retrieve_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/auth/retrieve/ url.
        :return: None
        """
        url = reverse('auth-retrieve')
        self.assertEquals(resolve(url).func.view_class, RetriveUserView)

    def test_total_users_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/super/total/users/ url.
        :return: None
        """
        url = reverse('get-total-users')
        self.assertEquals(resolve(url).func.view_class, TotalNumberOfUserView)

    def test_search_user_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/super/search/status/<str:is_active>/<str:is_reviewer>/<str:is_staff>/<str:is_superuser>/date_range/<str:search_option>/<str:start_date>/<str:end_date>/id_range/<str:start_id>/<str:end_id>/submission_range/<str:start_submission>/<str:end_submission>/search_value/ url.
        :return: None
        """
        url = reverse('search-anything-by-filter-date-id',
                      args=[
                          "is_active",
                          "is_reviewer",
                          "is_staff",
                          "is_superuser",
                          "search_option",
                          "start_date",
                          "end_date",
                          "start_id",
                          "end_id",
                          "start_submission",
                          "end_submission"
                      ]
                      )
        self.assertEquals(resolve(url).func.view_class, SearchByAnythingWithFilterDateIdView)
