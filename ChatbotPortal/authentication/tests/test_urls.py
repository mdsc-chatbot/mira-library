"""test_urls.py: Backend API tests for URLs declared in authentication app."""

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
                     UpdateSubmissionsView, UpdateApprovedSubmissionsView, TotalNumberOfUserView,
                     SearchByAnythingWithFilterDateIdView, UpdatePasswordView)


class TestUrls(SimpleTestCase):
    """
    Tests the urls redirected from http://127.0.0.1:8000/signup/
    """

    def test_currentuser_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/chatbotportal/authorization/currentuser/ url.
        :return: None
        """
        url = reverse('auth-current-user')
        self.assertEquals(resolve(url).func.view_class, CurrentUserView)

    def test_login_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/login url.
        :return: None
        """
        url = reverse('auth-login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/chatbotportal/authorization/logout/ url.
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
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/register url.
        :return: None
        """
        url = reverse('auth-register')
        self.assertEquals(resolve(url).func.view_class, RegisterUsersView)

    def test_update_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/<pk>/update/ url.
        :return: None
        """
        url = reverse('auth-update', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdateUserView)

    def test_update_submissions_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/<pk>/update/submissions/ url.
        :return: None
        """
        url = reverse('auth-update-submissions', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdateSubmissionsView)

    def test_update_approved_submissions_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/<pk>/update/approved_submissions url.
        :return: None
        """
        url = reverse('auth-update-approved-submissions', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class,
                          UpdateApprovedSubmissionsView)

    def test_update_password_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/<pk>/update/password/ url.
        :return: None
        """
        url = reverse('auth-update-password', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UpdatePasswordView)

    def test_PasswordResetView_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/password/reset/ url.
        :return: None
        """
        url = reverse('password-reset')
        self.assertEquals(resolve(url).func.view_class, PasswordResetView)

    def test_PasswordResetConfirmView_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/password/reset/confirm/<uidb64>/<token>/ url.
        :return: None
        """
        url = reverse('password_reset_confirm', args=['MO', 'adsa654sdft4532esdhfg'])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_delete_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/chatbotportal/authorization/delete/<pk> url.
        :return: None
        """
        url = reverse('auth-delete', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, DeleteUserView)

    def test_retrieve_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/chatbotportal/authorization/retrieve/ url.
        :return: None
        """
        url = reverse('auth-retrieve')
        self.assertEquals(resolve(url).func.view_class, RetriveUserView)

    def test_total_users_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/chatbotportal/authorization/super/total/users/ url.
        :return: None
        """
        url = reverse('get-total-users')
        self.assertEquals(resolve(url).func.view_class, TotalNumberOfUserView)

    def test_search_user_url(self):
        """
        Tests the http://127.0.0.1:8000/chatbotportal/authorization/super/search/status/<str:is_active>/<str:is_reviewer>/<str:is_staff>/<str:is_superuser>/date_range/<str:search_option>/<str:start_date>/<str:end_date>/id_range/<str:start_id>/<str:end_id>/submission_range/<str:start_submission>/<str:end_submission>/<str:submission_range_option>/search_value/ url.
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
                          "end_submission",
                          "submission_range_option",
                      ]
                      )
        self.assertEquals(resolve(url).func.view_class, SearchByAnythingWithFilterDateIdView)
