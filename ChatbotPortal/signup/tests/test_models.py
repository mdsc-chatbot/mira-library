from django.test import TestCase
from ..models import User

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name = 'TESTMODEL',
            last_name = 'testmodel',
            email = 'testmodel@testmodel.ca',
            affiliation = 'testing model',
            password = '1234'
        )

    def test_user_is_created(self):
        new_user = User.objects.get(email = 'testmodel@testmodel.ca')
        self.assertEquals(new_user.first_name, self.user.first_name)

    def test_is_active(self):
        new_user = User.objects.get(email='testmodel@testmodel.ca')
        self.assertTrue(new_user.is_active)

    def test_is_staff(self):
        new_user = User.objects.get(email='testmodel@testmodel.ca')
        self.assertFalse(new_user.is_staff)

    def test_is_admin(self):
        new_user = User.objects.get(email='testmodel@testmodel.ca')
        self.assertFalse(new_user.is_admin)
