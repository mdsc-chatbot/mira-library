"""test_serializers.py: Backend API tests for serializers created for authentication app."""

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

from django.test import TestCase

from ..api.serializers import CustomUserSerializer, CustomUserTokenSerializer, UserUpdateSerializer
from ..models import CustomUser


class TestSerializers(TestCase):
    """
    Testing the serializers
    """

    def setUp(self):
        """
        Creating CustomUser model, and serializing the model using various serializer.
        :return: None
        """
        self.key_attributes = [
            'id',
            'last_login',
            'email',
            'first_name',
            'last_name',
            'affiliation',
            'date_joined',
            'is_active',
            'is_reviewer',
            'is_staff',
            'is_superuser',
            'profile_picture',
            'submissions',
            'pending_submissions',
            'approved_submissions',
            'points',
        ]
        self.user_attributes = {
            'id': 1,
            'email': 'test@user.ca',
            'password': '1234',
            'first_name': 'Test',
            'last_name': 'User',
            'affiliation': 'Tester',
            'is_active': True,
            'is_reviewer': False,
            'is_staff': False,
            'is_superuser': False,
        }

        self.user = CustomUser.objects.create(**self.user_attributes)

        self.custom_user_serializer = CustomUserSerializer(instance=self.user)
        self.custom_user_token_serializer = CustomUserTokenSerializer(instance=self.user)
        self.user_update_serializer = UserUpdateSerializer(instance=self.user)

    def test_CustomUserSerializer_has_expected_fields(self):
        """
        This function checks if the CustomUserSerializer has expected fields
        :return: None
        """
        data = self.custom_user_serializer.data
        self.assertSetEqual(set(data.keys()), set(self.key_attributes))

    def test_CustomUserTokenSerializer_has_expected_fields(self):
        """
        This function checks if the CustomUserTokenSerializer has expected fields
        :return: None
        """

        data = self.custom_user_token_serializer.data
        # Before adding token attribute to the key_attributes
        self.assertNotEqual(set(data.keys()), set(self.key_attributes))
        # After adding token attribute to the key_attributes
        self.key_attributes.append('token')
        self.assertEqual(set(data.keys()), set(self.key_attributes))

    def test_UserUpdateSerializer_has_expected_fields(self):
        """
        This function checks if the UserUpdateSerializer has expected fields
        :return: None
        """
        data = self.user_update_serializer.data
        # Serialized fields are not same as the fields in key_attributes
        self.assertNotEqual(set(data.keys()), set(self.key_attributes))
        self.assertEqual(set(data.keys()),
                         {'first_name', 'last_name', 'profile_picture'})

    def test_field_content(self):
        """
        This function checks if the fields are valid after serializer
        :return: None
        """
        regular = self.custom_user_serializer.data
        tokenized = self.custom_user_token_serializer.data
        updated = self.user_update_serializer.data

        self.assertEquals(regular['first_name'], self.user_attributes['first_name'])
        self.assertEquals(tokenized['first_name'], self.user_attributes['first_name'])
        self.assertEquals(updated['first_name'], self.user_attributes['first_name'])

        self.assertEquals(regular['last_name'], self.user_attributes['last_name'])
        self.assertEquals(tokenized['last_name'], self.user_attributes['last_name'])
        self.assertEquals(updated['last_name'], self.user_attributes['last_name'])

        self.assertEquals(regular['affiliation'], self.user_attributes['affiliation'])
        self.assertEquals(tokenized['affiliation'], self.user_attributes['affiliation'])
        self.assertNotIn('affiliation', updated)

        self.assertNotIn('password', regular)
        self.assertNotIn('password', tokenized)
        self.assertNotIn('password', updated)

        self.assertNotIn('token', regular)
        self.assertIn('token', tokenized)
        self.assertNotIn('token', updated)

        self.assertIn('id', regular)
        self.assertIn('id', tokenized)
        self.assertNotIn('id', updated)

    def test_serializers_are_picking_on_invalid_values(self):
        """
        This function checks if the serializer serializes valid data
        :return: None
        """

        regular = CustomUserSerializer(instance=self.user, data=self.user_attributes)
        self.assertTrue(regular.is_valid())

        tokenized = CustomUserTokenSerializer(instance=self.user, data=self.user_attributes)
        self.assertTrue(tokenized.is_valid())

        updated = UserUpdateSerializer(instance=self.user, data=self.user_attributes)
        self.assertTrue(updated.is_valid())
