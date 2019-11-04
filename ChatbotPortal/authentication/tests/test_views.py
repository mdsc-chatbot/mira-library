import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, NoReverseMatch
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

    def login_client(self, email='', password=''):
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
        # assert token key exists
        self.assertIn('token', response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test login with invalid credentials
        response = self.login_a_user('anonymous', 'whoareyou')
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_of_registed_user(self):
        """
        Testing the login permission of different registered user.
        :return: None
        """

        # register with valid credentials who needs an email verification
        user = CustomUser.objects.create_user(
            email='new@user.com',
            password='1234',
            first_name='NewTestUser',
            last_name='NewTestUser',
            affiliation='Tester',
            is_active=False
        )

        # Login before email verification
        response = self.login_a_user('new@user.com', '1234')
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assuming the email is verified
        user.is_active = True
        user.save()
        # Login after email verification
        response = self.login_a_user('new@user.com', '1234')
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

        # Checking authorization, login a user without setting authorization token
        self.login_a_user('user@update.com', '1234')

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
        # assert status code is 401_UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Checking authorization, login a user and setting authorization token
        self.login_client('user@update.com', '1234')

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

        # assert status code is 200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # getting the user from the database using primary key
        self.user = CustomUser.objects.get(id=pk)
        # checking the user's information after updating
        self.assertEqual(self.user.email, 'user@update.com')
        self.assertEqual(self.user.first_name, 'AfterUpdate')
        self.assertEqual(self.user.last_name, 'AfterUpdate')
        self.assertNotEqual(self.user.first_name, 'BeforeUpdate')
        self.assertNotEqual(self.user.last_name, 'BeforeUpdate')


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


class TestCurrentUserView(BaseViewTest):
    """
    Tests for auth/currentuser endpoint
    """

    def setUp(self):
        """
        This constructor creates a regular user.
        :return: None
        """
        self.regular_user1 = CustomUser.objects.create_user(
            email='regular@user.ca',
            password='5678',
            first_name='regular',
            last_name='regular',
            affiliation='TestingCurrentUserView',
        )

    def test_current_user_view(self):
        """
        This method tests for various scenarios for retrieving a current user.
        :return: None
        """

        url = reverse('auth-current-user')

        # Check for current user after login a user
        self.login_client('regular@user.ca', '5678')

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['email'], 'regular@user.ca')
        self.assertIn('token', response.data)

        # Check for current user after logout a user
        self.client.logout()

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert response data is empty
        self.assertIsNone(response.data)


class TestLogoutView(BaseViewTest):
    """
    Tests for auth/logout/ endpoint
    """

    def setUp(self):
        """
        This constructor creates a regular user.
        :return: None
        """
        self.regular_user = CustomUser.objects.create_user(
            email='regular@user.ca',
            password='5678',
            first_name='regular',
            last_name='regular',
            affiliation='TestingLogout',
        )

    def test_logging_out_a_user(self):
        """
        This function tests for logout scenarios.
        :return: None
        """

        # Login the regular user
        self.login_client('regular@user.ca', '5678')

        # Calling logout API
        logout_url = reverse('auth-logout')
        response = self.client.get(logout_url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'AnonymousUser')

        # Regular logout operation does not work on the testing module
        # once a user is logged in through testing, so needs to use client
        # logout operation from APIClient
        self.client.logout()

        # Trying to retrieve the current user which should not be returned
        current_user_url = reverse('auth-current-user')
        response = self.client.get(current_user_url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert response data is empty
        self.assertIsNone(response.data)


class TestAllUsersView(BaseViewTest):
    """
    Tests for super/search/alluser/ endpoint
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
            affiliation='TestGettingAllUserList',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingAllUserList'
        )

        self.url = reverse('search-alluser')

    def test_AllUsersView_by_regular_user(self):
        """
        This function tests whether a regular user can view all the user details.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')
        response = self.client.get(self.url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_AllUsersView_by_super_user(self):
        """
        This function tests whether a super user can view all the user details.
        :return: None
        """
        self.login_client('super@user.ca', '1234')
        response = self.client.get(self.url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[2]['email'], 'regular2@user.ca')


class TestSearchByDateRangeView(BaseViewTest):
    """
    Tests for super/search/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/ endpoint
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
            affiliation='TestGettingUsersByDateRange',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingUsersByDateRange'
        )

    def test_SearchByDateRangeView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')

        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'last_login',
                'start_date': '2010-01-01',
                'end_date': '2020-01-01'
            }
        )
        response = self.client.get(url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_SearchByDateRangeView_by_super_user(self):
        """
        This function tests whether a super user can search users based on a range of either last_login or joined_date.
        :return: None
        """

        # Having another user logged in so that we can have more than one user in the search list
        self.login_client('regular1@user.ca', '5678')
        # Logging in super user
        self.login_client('super@user.ca', '1234')

        # Last login test using valid url
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'last_login',
                'start_date': '2010-01-01',
                'end_date': '2020-01-01'
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The length of response data should be 2 since 2 users were logged in
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')

        # logging in another user
        self.login_client('regular2@user.ca', '4321')
        # logging in super user
        self.login_client('super@user.ca', '1234')
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The length of response data should be 3 since 3 users were logged in
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[2]['email'], 'regular2@user.ca')

        # Last login test using valid url, when no login in formation was found
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'last_login',
                'start_date': '2010-01-01',
                'end_date': '2015-01-01'
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The length of response data should be 0
        self.assertEqual(len(response.data), 0)

        # Last login test using invalid date
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'last_login',
                'start_date': 'ggg',
                'end_date': 'kkk'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The query returns nothing
        self.assertEqual(len(response.data), 0)

        # date_joined test using valid url
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'date_joined',
                'start_date': '2010-01-01',
                'end_date': '2020-01-01'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response data should have length of 3, since 3 users were created
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[2]['email'], 'regular2@user.ca')

        # date_joined test using valid url, when no account was created
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'date_joined',
                'start_date': '2010-01-01',
                'end_date': '2015-01-01'
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The length of response data should be 0
        self.assertEqual(len(response.data), 0)

        # date_joined test using invalid date
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'date_joined',
                'start_date': 'invalid-date',
                'end_date': 'date-invalid'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response data should have length of 0
        self.assertEqual(len(response.data), 0)

        # testing invalid search option, search option must be either, date_joined or last_login
        url = reverse(
            'search-by-date-range',
            kwargs={
                'search_option': 'invalid search option',
                'start_date': '2010-01-01',
                'end_date': '2020-01-01'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response data should have length of 0
        self.assertEqual(len(response.data), 0)


class TestSearchByIdRangeView(BaseViewTest):
    """
    Tests for super/search/id_range/<int:start_id>/<int:end_id>/ endpoint
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
            affiliation='TestGettingUsersByIdRange',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingUsersByIdRange'
        )

    def test_SearchByIdRangeView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')

        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 1,
                'end_id': 100
            }
        )
        response = self.client.get(url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_SearchByIdRangeView_by_super_user(self):
        """
        This function tests whether a super user can search users based on a range of ids.
        :return: None
        """
        self.login_client('super@user.ca', '1234')

        # Search with a valid id range that have users
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 1,
                'end_id': 10
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[2]['email'], 'regular2@user.ca')

        # Search with a valid id range that do not have users
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 5,
                'end_id': 10
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # start_id = 0
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 0,
                'end_id': 10
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # end_id = 0
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 0,
                'end_id': 0
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # start_id < end_id
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 3,
                'end_id': 2
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # start_id = end_id
        url = reverse(
            'search-by-id-range',
            kwargs={
                'start_id': 2,
                'end_id': 2
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'regular1@user.ca')

        # start_id < 0, end_id < 0
        try:
            reverse(
                'search-by-id-range',
                kwargs={
                    'start_id': -2,
                    'end_id': -2
                }
            )
        except NoReverseMatch:
            # The url fails to match
            self.assertRaises(NoReverseMatch)


class TestSearchByAnythingView(BaseViewTest):
    """
    Tests for super/search/by_anything/ endpoint
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
            affiliation='TestGettingUsersByAnything',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingUsersByAnything'
        )

    def test_SearchByAnythingView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')
        url = reverse('search-by-anything')

        response = self.client.get(url, data={'search': 'Test'})
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_SearchByAnythingView_by_super_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('super@user.ca', '1234')
        url = reverse('search-by-anything')

        # Search for a valid item, that exists
        response = self.client.get(url, data={'search': 'Test'})
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular2@user.ca')

        # Search for a valid item, that exists
        response = self.client.get(url, data={'search': 'regular1'})
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'regular1@user.ca')

        # Search for a valid item, that does not exist
        response = self.client.get(url, data={'search': 'regular11'})
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestSearchFilterUserView(BaseViewTest):
    """
    Tests for super/search/filter/<str:filter_by>/<str:filter_value>/ endpoint
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
            affiliation='TestGettingFilteredUser',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingFilteredUser'
        )

    def test_SearchFilterUserView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'is_active',
                'filter_value': True
            }
        )

        response = self.client.get(url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_SearchByAnythingView_by_super_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('super@user.ca', '1234')

        # Search for valid filter_by option with valid filter_value
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'is_active',
                'filter_value': True
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')
        self.assertEqual(response.data[1]['email'], 'regular1@user.ca')
        self.assertEqual(response.data[2]['email'], 'regular2@user.ca')

        # Search for valid filter_by option with valid filter_value
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'is_superuser',
                'filter_value': True
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')

        # Search for invalid filter_by option with valid filter_value
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'first_name',
                'filter_value': True
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Search for valid filter_by option with invalid filter_value
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'is_active',
                'filter_value': 'true'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Search for invalid filter_by option with invalid filter_value
        url = reverse(
            'search-filter-user',
            kwargs={
                'filter_by': 'last_login',
                'filter_value': 'true'
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestTotalNumberOfUserView(BaseViewTest):
    """
    Tests for super/total/users/ endpoint
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
            affiliation='TestGettingFilteredUser',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingFilteredUser'
        )

    def test_TotalNumberOfUserView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')
        url = reverse('get-total-user')

        response = self.client.get(url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_TotalNumberOfUserView_by_super_user(self):
        """
        This function tests whether a super user can perform a search operation.
        :return: None
        """
        self.login_client('super@user.ca', '1234')

        url = reverse('get-total-user')

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_count', response.data)
        self.assertEqual(response.data['user_count'], 3)


class TestRangeOfUsersView(BaseViewTest):
    """
    Tests for super/rows/<int: start_row>/<int: end_row> endpoint
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
            affiliation='TestGettingFilteredUser',
        )
        self.regular_user2 = CustomUser.objects.create_user(
            email='regular2@user.ca',
            password='4321',
            first_name='regular2',
            last_name='regular2',
            affiliation='TestGettingFilteredUser'
        )

    def test_TotalNumberOfUserView_by_regular_user(self):
        """
        This function tests whether a regular user can perform a search operation.
        :return: None
        """
        self.login_client('regular1@user.ca', '5678')
        # Search for invalid filter_by option with invalid filter_value
        url = reverse(
            'get-rows',
            kwargs={
                'start_row': 0,
                'end_row': 1
            }
        )

        response = self.client.get(url)
        # assert status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_TotalNumberOfUserView_by_super_user(self):
        """
        This function tests whether a super user can perform a search operation.
        :return: None
        """
        self.login_client('super@user.ca', '1234')

        # Search for valid row range
        url = reverse(
            'get-rows',
            kwargs={
                'start_row': 0,
                'end_row': 1
            }
        )

        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'super@user.ca')

        # Search for invalid row range
        url = reverse(
            'get-rows',
            kwargs={
                'start_row': 5,
                'end_row': 4
            }
        )
        response = self.client.get(url)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)



"""
References
1. https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-part-2-cfb87e2c8a6c
2. https://medium.com/@MicroPyramid/introduction-to-api-development-with-django-rest-framework-807f992a74b3
"""