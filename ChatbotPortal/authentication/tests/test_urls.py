from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import (LoginView,
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
                     )


class TestUrls(SimpleTestCase):
    """
    Tests the urls redirected from http://127.0.0.1:8000/signup/
    """

    def test_login_url(self):
        """
        Tests the http://127.0.0.1:8000/authorization/auth/login url.
        :return: None
        """
        url = reverse('auth-login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

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

    def test_currentuser_url(self):
        """
        Tests the Tests the http://127.0.0.1:8000/authorization/auth/currentuser/ url.
        :return: None
        """
        url = reverse('auth-current-user')
        self.assertEquals(resolve(url).func.view_class, CurrentUserView)

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

    def test_all_users_url(self):
        """
        Tests the Tests the super/search/alluser/ url.
        :return: None
        """
        url = reverse('search-alluser')
        self.assertEquals(resolve(url).func.view_class, AllUsersView)

    def test_search_by_date_range_url(self):
        """
        Tests the super/search/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/ url.
        :return: None
        """
        url = reverse('search-by-date-range', args=['search_option', '1999-AA-BB', '20A-BB-C'])
        self.assertEquals(resolve(url).func.view_class, SearchByDateRangeView)

    def test_search_by_id_range_url(self):
        """
        Tests the super/search/id_range/<int:start_id>/<int:end_id>/ url.
        :return: None
        """
        url = reverse('search-by-id-range', args=["1", "2"])
        self.assertEquals(resolve(url).func.view_class, SearchByIdRangeView)

    def test_search_by_anything_url(self):
        """
        Tests the super/search/by_anything/ url.
        :return: None
        """
        url = reverse('search-by-anything')
        self.assertEquals(resolve(url).func.view_class, SearchByAnythingView)

    def test_search_filter_user_url(self):
        """
        Tests the super/search/filter/<str:filter_by>/<str:filter_value>/ url.
        :return: None
        """
        url = reverse('search-filter-user', args=["filter_by", "filter_value"])
        self.assertEquals(resolve(url).func.view_class, SearchFilterUserView)
