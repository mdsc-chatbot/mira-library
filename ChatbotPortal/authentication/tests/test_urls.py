from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import LoginView, RegisterUsersView, UpdateUserView, DeleteUserView


class TestUrls(SimpleTestCase):
    """
    Tests the urls redirected from http://127.0.0.1:8000/signup/
    """

    # def test_current_user_url_is_resolved(self):
    #     url = reverse('current_user')
    #     self.assertEquals(resolve(url).func, current_user)
    #
    # def test_UserCreateList_url_is_resolved(self):
    #     url = reverse('user_create_list')
    #     self.assertEquals(resolve(url).func.view_class, UserCreateList)
    #
    # def test_UserUpdateList_url_is_resolved(self):
    #     url = reverse('user_update', args=['some-pk'])
    #     self.assertEquals(resolve(url).func.view_class, UserUpdateList)

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
