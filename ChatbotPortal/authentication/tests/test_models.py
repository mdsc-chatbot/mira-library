"""test_models.py: Backend API tests for CustomUser model related functions."""

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

from django.contrib.auth import get_user_model
from django.test import TestCase


class TestModels(TestCase):
    """
    This class tests the CustomUser model
    Reference: https://testdriven.io/blog/django-custom-user-model/
    """

    def setUp(self):
        """
        The constructor that will run before every test.
        :return: None
        """
        # Getting the user model used in this project
        self.User = get_user_model()

    def test_create_user(self):
        """
        Tests for regular user.
        :return: None
        """
        user = self.User.objects.create_user(
            email='test@user.ca',
            password='1234'
        )
        self.assertEqual(user.email, 'test@user.ca')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_reviewer)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        # Create user while no parameter is provided
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

        # Create user while empty email field is provided, but password field is absent
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='')

        # Create user while empty email field is provided and password field is present
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password='1234')

    def test_create_superuser(self):
        """
        Test for super user.
        :return: None
        """
        admin_user = self.User.objects.create_superuser(
            email='super@user.ca',
            password='1234'
        )
        self.assertEqual(admin_user.email, 'super@user.ca')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_reviewer)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        # Trying to create a super user with is_superuser as false
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                is_superuser=False
            )
