import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import CustomUser


class BaseViewTest(APITestCase):
    """
    A class with required authentication related functions.
    """

    # Defining the APIClient to call APIs
    client = APIClient()

    def setUp(self):
        """
        This constructor creates a super user.
        :return: None
        """
        # create an admin user
        self.user = CustomUser.objects.create_superuser(
            email='test@super.com',
            password='1234',
            first_name='Test',
            last_name='Super'
        )

    def login_a_user(self, email='', password=''):
        """
        A function that calls LoginView API from the views
        :param email: user email
        :param password: user password
        :return: Response for a logged in client
        """
        url = reverse('auth-login')
        # performing POST request for login
        return self.client.post(
            url,
            data=json.dumps({
                'email': email,
                'password': password
            }),
            content_type='application/json'
        )

    def login_client(self, email="", password=""):
        """
        To be used for generating HTTP Authorization header upon login.
        :param email: user email
        :param password: user password
        :return: The generated token
        """
        # get a token from DRF
        # performing POST request for login
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps({
                'email': email,
                'password': password
            }),
            content_type='application/json'
        )

        self.token = response.data['token']

        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )

        # Let the client login after the authentication
        self.client.login(email=email, password=password)

        return self.token

    def register_a_user(self, email='', password='', first_name='', last_name='', affiliation=''):
        """
        This definition registers/creates a new user.
        :param email: user email
        :param password: user password
        :param first_name: user's first name
        :param last_name: user's last name
        :param affiliation: user's affiliation to the service
        :return: Response for a registered user
        """
        url = reverse('auth-register')
        # Performing POST requests to create a user
        return self.client.post(
            url,
            data=json.dumps({
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'affiliation': affiliation
            }),
            content_type='application/json'
        )


class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user(self):
        """
        This definition tests for login operation with various user credentials
        :return: None
        """

        # test login with valid credentials
        response = self.login_a_user('test@super.com', '1234')
        print(response.data)
        # assert token key exists
        self.assertIn('token', response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test login with invalid credentials
        response = self.login_a_user('anonymous', 'whoareyou')
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    """
    Tests for auth/register/ endpoint
    """

    def test_register_a_user(self):
        """
        This definition tests for user registration with various scenarios.
        :return: None
        """

        # register with valid credentials
        response = self.register_a_user(
            email='new@user.com',
            password='1234',
            first_name='NewTestUser',
            last_name='NewTestUser',
            affiliation='Tester'
        )
        # assert status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test register with invalid credentials
        response = self.register_a_user('', '', '', '', '')
        # assert status code is 400 BAD_REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserTest(BaseViewTest):
    """
    Tests for auth/<pk>/update/ endpoint
    """

    def setUp(self):
        """
        This constructor creates a regular user
        :return: None
        """
        self.user = CustomUser.objects.create_user(
            email='user@update.com',
            password='1234',
            first_name='BeforeUpdate',
            last_name='BeforeUpdate',
            affiliation='UpdateTester'
        )

    def test_update_user(self):
        """
        This definition tests for various user update scenarios.
        :return: None
        """

        # checking the user's information before updating
        self.assertEqual(self.user.email, 'user@update.com')
        self.assertEqual(self.user.first_name, 'BeforeUpdate')
        self.assertEqual(self.user.last_name, 'BeforeUpdate')
        self.assertNotEqual(self.user.first_name, 'AfterUpdate')
        self.assertNotEqual(self.user.last_name, 'AfterUpdate')

        # test login with valid credentials before updating
        response = self.login_a_user('user@update.com', '1234')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # let the user login to generate token
        token = self.login_client('user@update.com', '1234')

        # primary key of the user to be updated
        pk = self.user.id
        url = reverse(
            'auth-update',
            kwargs={
                'pk': pk
            }
        )

        # Performing PUT request to update a user.
        response = self.client.put(
            url,
            data=json.dumps({
                'first_name': 'AfterUpdate',
                'last_name': 'AfterUpdate',
                'password': '5678'
            }),
            content_type='application/json'
        )
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # getting the user from the database using primary key
        self.user = CustomUser.objects.get(id=pk)
        # checking the user's information after updating
        self.assertEqual(self.user.email, 'user@update.com')
        self.assertEqual(self.user.first_name, 'AfterUpdate')
        self.assertEqual(self.user.last_name, 'AfterUpdate')
        self.assertNotEqual(self.user.first_name, 'BeforeUpdate')
        self.assertNotEqual(self.user.last_name, 'BeforeUpdate')

        # test login with credentials before updating
        response = self.login_a_user('user@update.com', '1234')
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test login with credentials after updating
        response = self.login_a_user('user@update.com', '5678')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(BaseViewTest):
    """
    Tests for auth/delete/<pk>/ endpoint
    """

    def setUp(self):
        """
        This constructor creates a super user and two regular users.
        :return: None
        """
        self.super_user = CustomUser.objects.create_superuser(
            email='super@user.ca',
            password='1234'
        )
        self.regular_user1 = CustomUser.objects.create_user(
            email='regular1@user.ca',
            password='5678',
            first_name='regular1',
            last_name='regular1',
            affiliation='DeleteTesterAsRegularUserToDelete',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='DeleteTesterAsRegularUserToBeDeleted'
        )

    def test_delete_user_by_regular_user(self):
        """
        This definition tests if a regular user can delete other users.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')

        # primary key of the user to be deleted
        pk_to_delete = self.regular_user2.id

        url = reverse(
            'auth-delete',
            kwargs={
                'pk': pk_to_delete
            }
        )

        # perform DELETE request to delete APIs
        response = self.client.delete(
            url,
            data=json.dumps({
                'id': pk_to_delete
            }),
            content_type='application/json'
        )
        # assert status code is 403 FORBIDDEN, meaning the logged in user does not have access
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # checking if the user to be deleted still exists in the database
        self.assertEqual(get_object_or_404(CustomUser, id=pk_to_delete), self.regular_user2)

    def test_delete_user_by_super_user(self):
        """
        This definition tests if a super user can delete other users.
        :return: None
        """

        self.login_client('super@user.ca', '1234')

        pk_to_delete = self.regular_user2.id

        url = reverse(
            'auth-delete',
            kwargs={
                'pk': pk_to_delete
            }
        )

        # perform DELETE request to call delete APIs
        response = self.client.delete(
            url,
            data=json.dumps({
                'id': pk_to_delete
            }),
            content_type='application/json'
        )
        # assert status code is 204 NO_CONTENT, means the user has been deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # checking if the deleted user still exists in the database
        with self.assertRaises(Http404):
            get_object_or_404(CustomUser, id=pk_to_delete)

        # trying to delete the user once again
        response = self.client.delete(
            url,
            data=json.dumps({
                'id': pk_to_delete
            }),
            content_type='application/json'
        )
        # assert status code is 404 NOT_FOUND, because the user has already been deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RetrieveUserTest(BaseViewTest):
    """
    Tests for auth/retrieve/ endpoint
    """
    def setUp(self):
        self.regular_user = CustomUser.objects.create_user(
            email='regular@user.ca',
            password='5678',
            first_name='regular',
            last_name='regular',
            affiliation='RetrieveTester',
        )

        self.url = reverse('auth-retrieve')

    def test_retrieve_user(self):
        """
        This definition tests if a user can be retrieved.
        :return: None
        """
        # trying to retrieve without logging in
        response = self.client.get(self.url)
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # trying to retrieve after logging in
        self.login_client('regular@user.ca', '5678')
        response = self.client.get(self.url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.regular_user.id)
        self.assertEqual(response.data['first_name'], self.regular_user.first_name)
        self.assertEqual(response.data['last_name'], self.regular_user.last_name)
        self.assertEqual(response.data['affiliation'], self.regular_user.affiliation)




"""
References
1. https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-part-2-cfb87e2c8a6c
2. https://medium.com/@MicroPyramid/introduction-to-api-development-with-django-rest-framework-807f992a74b3
"""
