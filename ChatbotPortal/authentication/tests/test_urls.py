from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import LoginView, RegisterUsersView, UpdateUserView, DeleteUserView, activate, CurrentUserView, LogoutView, \
    RetriveUserView


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
