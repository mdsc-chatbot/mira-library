from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import UserCreateList, UserUpdateList, current_user

class TestUrls(SimpleTestCase):

    def test_current_user_url_is_resolved(self):
        url = reverse('current_user')
        self.assertEquals(resolve(url).func, current_user)

    def test_UserCreateList_url_is_resolved(self):
        url = reverse('user_create_list')
        self.assertEquals(resolve(url).func.view_class, UserCreateList)

    def test_UserUpdateList_url_is_resolved(self):
        url = reverse('user_update', args=['some-pk'])
        self.assertEquals(resolve(url).func.view_class, UserUpdateList)