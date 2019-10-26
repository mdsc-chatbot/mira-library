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
