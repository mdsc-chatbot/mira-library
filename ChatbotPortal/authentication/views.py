"""views.py: Authentication app related API views are declared here.
            It comprises CurrentUserView, LoginView, LogoutView, RegisterUsersView,
            UpdateUserView, UpdateUserByAdminView, DeleteUserView, UpdateSubmissionsView,
            UpdateApprovedSubmissionsView, TotalNumberOfUserView, SearchByAnythingWithFilterDateIdView,
            UpdatePasswordView."""

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

import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import filters
from rest_framework import permissions, status, generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .api.paginators import ChatBotPaginator
from .api.serializers import (CustomUserSerializer,
                              CustomUserTokenSerializer,
                              UserUpdateSerializer,
                              UserUpdateSubmissionSerializer,
                              UserUpdateApprovedSubmissionSerializer,
                              UserUpdatePasswordSerializer,
                              UserUpdateByAdminSerializer)
from .email_manager.email_tokens import account_activation_token
from .models import CustomUser

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CurrentUserView(generics.RetrieveAPIView):
    """
    GET chatbotportal/authentication/currentuser
    Retrive User API
    """
    permission_classes = (permissions.AllowAny,)  # anyone can have access

    def get(self, request, *args, **kwargs):
        """
        A get method for getting the current user who is already logged in.
        reference: https://stackoverflow.com/questions/8000040/how-to-get-logged-in-users-uid-from-session-in-django
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        # logout(request)
        # Check if the request has a session associated with it
        # if bool(request.session.session_key):
        #     # if bool(request.session._session):
        #     session_key = request.session.session_key
        #     session = Session.objects.get(session_key=session_key)
        #     session_data = session.get_decoded()
        #     uid = session_data.get('_auth_user_id')
        #     # uid = request.session._session['_auth_user_id']
        #     user = CustomUser.objects.get(id=uid)

        #     if user is not None:
        #         serializer = CustomUserTokenSerializer(user, context={'request': request})
        #         return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        user = request.user
        print(user)
        if user.is_authenticated:
            serializer = CustomUserTokenSerializer(user, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

class LoginView(generics.CreateAPIView):
    """
    POST chatbotportal/authentication/login
    Login API
    """
    # This permission class will override the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)  # Anyone can access
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        A post method for letting user login
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        # authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # login saves the user's ID in the session
            login(request, user)
            # ***************Use of context is a big question here!!!*************
            serializer = CustomUserTokenSerializer(user, context={'request': request}).data
            return Response(serializer)

        return Response(data={'message': 'Incorrect Email or Password! Please try again.'},
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class LogoutView(generics.RetrieveAPIView):
    """
    GET chatbotportal/authentication/logout
    Logout User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can have access

    def get(self, request, *args, **kwargs):
        """
        A get method for letting user logout.
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        logout(request)
        # If the user becomes anonymous, return HTTP_200_OK
        if request.user.is_anonymous:
            return Response(data={'user': 'AnonymousUser'}, status=status.HTTP_200_OK)

        # If the user is not anonymous, meaning no logout happened, return HTTP_400_BAD_REQUEST
        return Response(data={'user': 'NotAnonymousUser'}, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    """
    activate view function renders upon clicking the link sent on the email.
    references:
        1. https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
        2. https://blog.hlab.tech/part-ii-how-to-sign-up-user-and-send-confirmation-email-in-django-2-1-and-python-3-6/
    :param request: The link request sent from the email address
    :param uidb64: The base64 encoded primary key
    :param token: The token created from the User details
    :return: Response with serialized User, status value
    """
    try:
        # Decoding the uidb64 and transforming into text
        uid = force_text(urlsafe_base64_decode(uidb64))

        # Retrieving the user with such user id
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        # Assign user as None if no user is found with that id
        user = None

    # If the user exists and the token is similar, activate the user
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:8000/chatbotportal/app/login')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        # return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
    """
    POST chatbotportal/authentication/register/
    Registration API
    """
    permission_classes = (permissions.AllowAny,)  # Anyone can register

    def post(self, request, *args, **kwargs):
        """
        This post method creates a valid new user
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        email = request.data.get('email', )
        password = request.data.get('password', )
        first_name = request.data.get('first_name', )
        last_name = request.data.get('last_name', )
        affiliation = request.data.get('affiliation', )

        if not email and not password:
            return Response(
                data={
                    'message': 'Email and Password are required to register a user.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Checking if the email address was in valid format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                data={
                    'message': 'Not a valid email address.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify if the password is at least 8 characters long
        try:
            validate_password(password)
        except ValidationError:
            return Response(
                data={
                    'message': 'Not a valid email address.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                affiliation=affiliation,
                is_active=False
            )
        except IntegrityError:
            return Response(
                data={
                    'message': 'Email already exists. Please try a new email address.'
                },
                status=status.HTTP_226_IM_USED
            )

        # get the current site
        current_site = get_current_site(request)
        # setting email subject
        mail_subject = 'Activate ChatbotPortal'
        # setting email body through rendering
        # the json data into string to show on a html template
        message = render_to_string(
            'activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                # encoding the bytes of user's primary key
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # creating a token from the user's details
                'token': account_activation_token.make_token(user),
            }
        )

        # creating an Email message object with designated fields
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            to=[user.email, ]
        )

        email.content_subtype = "html"  # Main content is now text/html instead of plain text
        email.send()

        return Response(
            data={
                'message': 'An activation email has been sent to your email address. Please check your email. Thank you!'},
            status=status.HTTP_201_CREATED
        )


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """
    PUT chatbotportal/authentication/<pk>/update/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer


class UpdateUserByAdminView(generics.RetrieveUpdateAPIView):
    """
    PUT chatbotportal/authentication/<pk>/update/
    Update User API
    """
    permission_classes = (permissions.IsAdminUser,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateByAdminSerializer


class UpdateSubmissionsView(generics.RetrieveUpdateAPIView):
    """
    PUT chatbotportal/authentication/<pk>/update/submissions/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSubmissionSerializer


class UpdateApprovedSubmissionsView(generics.RetrieveUpdateAPIView):
    """
    PUT chatbotportal/authentication/<pk>/update/approved_submissions/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateApprovedSubmissionSerializer


class DeleteUserView(generics.DestroyAPIView):
    """
    DELETE chatbotportal/authentication/delete/<pk>/
    Delete User API
    """
    permission_classes = (permissions.IsAdminUser,)  # Only admin/super_user can delete any account
    queryset = CustomUser.objects.all()

    def delete(self, request, *args, **kwargs):
        """
        A delete method for deleting a registered user account.
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        try:
            instance = CustomUser.objects.get(id=kwargs['pk'])  # getting the User from the database
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CustomUser.DoesNotExist:
            # if the user does not exist, return 404 NOT_FOUND
            return Response(status=status.HTTP_404_NOT_FOUND)


class RetriveUserView(generics.RetrieveAPIView):
    """
    GET chatbotportal/authentication/retrieve
    Retrive User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can have access
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        """
        A get method for getting the current user's details.
        :param request: Request generated from the frontend form
        :param args: Non keyword arguments
        :param kwargs: Keyword arguments
        :return: Response of serialized data or status
        """
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


class TotalNumberOfUserView(generics.RetrieveAPIView):
    """
    GET super/total/users/
    Getting the number of total instance of model CustomUser
    """
    permission_classes = (permissions.IsAdminUser,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user_count = CustomUser.objects.count()
        content = {'user_count': user_count}
        return Response(content)


class SearchByAnythingWithFilterDateIdView(generics.ListAPIView):
    """
    GET uper/search/by_anything/
    Lists all users based on a search string (not case sensitive)
    """
    permission_classes = (permissions.IsAdminUser,)  # Only admin can perform this operation

    # Get all the instance of the model
    # queryset = CustomUser.objects.all().order_by('id')

    # Declare the serializer
    serializer_class = CustomUserSerializer

    pagination_class = ChatBotPaginator

    # Define backend search filter for drf
    filter_backends = (filters.SearchFilter,)

    # Define the attribute fields to be searched, must be present in the model
    search_fields = [
        'id',
        'email',
        'first_name',
        'last_name',
        'affiliation',
        'submissions',
        'points',
    ]

    def get_queryset(self):
        """
        This overrides the built-in get_queryset, in order to perform filtering operations.
        :return: filtered queryset
        """

        # Get all the instance of the model
        queryset = CustomUser.objects.all()

        is_active = self.kwargs['is_active']
        is_reviewer = self.kwargs['is_reviewer']
        is_staff = self.kwargs['is_staff']
        is_superuser = self.kwargs['is_superuser']

        search_option = self.kwargs['search_option']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        start_id = self.kwargs['start_id']
        end_id = self.kwargs['end_id']

        start_submission = self.kwargs['start_submission']
        end_submission = self.kwargs['end_submission']
        submission_range_option = self.kwargs['submission_range_option']

        if is_active != "''":
            try:
                queryset = queryset.filter(is_active=eval(is_active.capitalize()))
            except NameError:
                return queryset.none()

        if is_reviewer != "''":
            try:
                queryset = queryset.filter(is_reviewer=eval(is_reviewer.capitalize()))
            except NameError:
                return queryset.none()

        if is_staff != "''":
            try:
                queryset = queryset.filter(is_staff=eval(is_staff.capitalize()))
            except NameError:
                return queryset.none()

        if is_superuser != "''":
            try:
                queryset = queryset.filter(is_superuser=eval(is_superuser.capitalize()))
            except NameError:
                return queryset.none()

        if search_option != "''":
            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                # To get rid of run time warning of naive datetime incorporate current time zone
                current_timezone = timezone.get_current_timezone()
                start_date = current_timezone.localize(start_date)
                end_date = current_timezone.localize(end_date)

            except ValueError:
                return queryset.none()

            # Filter based on last logged in attributes
            if search_option == 'last_login':
                queryset = queryset.filter(last_login__range=(start_date, end_date))

                # Filter based on date_joined attributes
            elif search_option == 'date_joined':
                queryset = queryset.filter(date_joined__range=(start_date, end_date))

        if start_id != "''" or end_id != "''":
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                return queryset.none()

            # Checking if the start_id <= end_id and both the ids are greater than 0
            if 0 < start_id <= end_id and end_id > 0:
                queryset = queryset.filter(id__range=(start_id, end_id))
            else:
                return queryset.none()

        if start_submission != "''" or end_submission != "''":
            try:
                start_submission = int(start_submission)
                end_submission = int(end_submission)
            except ValueError:
                return queryset.none()

            # Checking if the start_id <= end_id and both the ids are greater than 0
            if 0 <= start_submission <= end_submission:
                if submission_range_option == "total":
                    queryset = queryset.filter(submissions__range=(start_submission, end_submission))
                elif submission_range_option == "pending":
                    queryset = queryset.filter(pending_submissions__range=(start_submission, end_submission))
                elif submission_range_option == "approved":
                    queryset = queryset.filter(approved_submissions__range=(start_submission, end_submission))
            else:
                return queryset.none()

        return queryset.order_by('id')


class UpdatePasswordView(generics.RetrieveUpdateAPIView):
    """
    PUT chatbotportal/authentication/<pk>/update/password/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdatePasswordSerializer


"""
References:
1. https://medium.com/swlh/searching-in-django-rest-framework-45aad62e7782
2. https://stackoverflow.com/questions/25151586/django-rest-framework-retrieving-object-count-from-a-model

"""
