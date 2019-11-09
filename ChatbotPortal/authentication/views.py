import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
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

from .api.serializers import CustomUserSerializer, CustomUserTokenSerializer, UserUpdateSerializer, UserUpdateSubmissionSerializer, UserUpdatePointSerializer
from .api.paginators import ChatBotPaginator
from .email_manager.email_tokens import account_activation_token
from .models import CustomUser

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login
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

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
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

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            affiliation=affiliation,
            is_active=False
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

        email.content_subtype= "html" # Main content is now text/html instead of plain text
        email.send()

        return Response(
            data={'message': 'To activate your portal, please confirm your email address.'},
            status=status.HTTP_201_CREATED
        )


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """
    PUT auth/<pk>/update/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer

class UpdateSubmissionsView(generics.RetrieveUpdateAPIView):
    """
    PUT auth/<pk>/update/submissions/
    Update User API
    """
    permission_classes = (permissions.AllowAny,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSubmissionSerializer

class UpdatePointsView(generics.RetrieveUpdateAPIView):
    """
    PUT auth/<pk>/update/submissions/
    Update User API
    """
    permission_classes = (permissions.AllowAny,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdatePointSerializer


class DeleteUserView(generics.DestroyAPIView):
    """
    DELETE auth/delete/<pk>/
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
    GET auth/retrieve
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


class CurrentUserView(generics.RetrieveAPIView):
    """
    GET auth/currentuser
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
        if bool(request.session.session_key):
            # if bool(request.session._session):
            session_key = request.session.session_key
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            uid = session_data.get('_auth_user_id')
            # uid = request.session._session['_auth_user_id']
            user = CustomUser.objects.get(id=uid)

            if user is not None:
                serializer = CustomUserTokenSerializer(user, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


class LogoutView(generics.RetrieveAPIView):
    """
    GET auth/logout
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


class AllUsersView(generics.ListAPIView):
    """
    GET super/search/alluser/
    Lists all users
    """
    permission_classes = (permissions.IsAdminUser, )  # Only admin can have access
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    pagination_class = ChatBotPaginator


class SearchByDateRangeView(generics.ListAPIView):
    """
    GET super/search/date_range/<str:search_option>/<slug:start_date>/<slug:end_date>/
    Lists all users based on a range of date
    """
    permission_classes = (permissions.IsAdminUser,)  # Only admin can perform this operation
    serializer_class = CustomUserSerializer
    pagination_class = ChatBotPaginator

    def get_queryset(self):
        """
        This overrides the built-in get_queryset, in order to perform filtering operations.
        :return: filtered queryset
        """
        # Get all the instance of the model
        queryset = CustomUser.objects.all()

        # Key words from path parameters
        search_option = self.kwargs['search_option']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        # Checks if the path parameter are of right value, otherwise return empty queryset
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
            return queryset.filter(last_login__range=(start_date, end_date)).order_by('id')

        # Filter based on date_joined attributes
        elif search_option == 'date_joined':
            return queryset.filter(date_joined__range=(start_date, end_date)).order_by('id')

        # If the search option was invalid, return empty queryset
        else:
            return queryset.none()


class SearchByIdRangeView(generics.ListAPIView):
    """
    GET super/search/id_range/<int:start_id>/<int:end_id>/
    Lists all users based on a range of ids
    """

    permission_classes = (permissions.IsAdminUser,)  # Only admin can perform this operation
    serializer_class = CustomUserSerializer
    pagination_class = ChatBotPaginator

    def get_queryset(self):
        """
        This overrides the built-in get_queryset, in order to perform filtering operations.
        :return: filtered queryset
        """

        # Get all the instance of the model
        queryset = CustomUser.objects.all()

        # Checking if valid id is coming from the path, otherwise return empty query
        try:
            start_id = int(self.kwargs['start_id'])
            end_id = int(self.kwargs['end_id'])
        except ValueError:
            return queryset.none()

        # Checking if the start_id <= end_id and both the ids are greater than 0
        if 0 < start_id <= end_id and end_id > 0:
            return queryset.filter(id__range=(start_id, end_id)).order_by('id')
        else:
            # Otherwise return empty query
            return queryset.none()


class SearchByAnythingView(generics.ListAPIView):
    """
    GET uper/search/by_anything/
    Lists all users based on a search string (not case sensitive)
    """
    permission_classes = (permissions.AllowAny,)  # Only admin can perform this operation

    # Get all the instance of the model
    queryset = CustomUser.objects.all().order_by('id')

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



class SearchFilterUserView(generics.ListAPIView):
    """
    GET super/search/filter/<str:filter_by>/<str:filter_value>/
    Lists all the filtered users based on either is_active, is_reviewer, is_staff, is_superuser
    """
    permission_classes = (permissions.AllowAny,)  # Only admin can perform this operation
    serializer_class = CustomUserSerializer
    pagination_class = ChatBotPaginator

    def get_queryset(self):
        """
        This overrides the built-in get_queryset, in order to perform filtering operations.
        :return: filtered queryset
        """

        # Get all the instance of the model
        queryset = CustomUser.objects.all()

        # Fields to be filtered
        filter_fields = ['is_active', 'is_reviewer', 'is_staff', 'is_superuser']

        # Key words from path parameters
        filter_by = self.kwargs['filter_by']
        filter_value = self.kwargs['filter_value']

        # If the filter_by value exists in filter_field, the filter the query
        if filter_by in filter_fields:
            try:
                return queryset.filter(**{filter_by: eval(filter_value)}).order_by('id')
            except NameError:
                # eval raises name error if the string is no exactly either 'True' or 'False'
                return queryset.none()
        else:
            return queryset.none()


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


class RangeOfUsersView(generics.ListAPIView):
    """
    GET super/rows/<int:start_id>/<int:end_id>/
    Lists users upto a certain row
    """

    permission_classes = (permissions.IsAdminUser,)  # Only admin can perform this operation
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        """
        This overrides the built-in get_queryset, in order to perform filtering operations.
        :return: filtered queryset
        """
        start_row = int(self.kwargs['start_row'])
        end_row = int(self.kwargs['end_row'])

        # Get all the instance of the model
        queryset = CustomUser.objects.all().order_by('id')[start_row:end_row]

        return queryset








class SearchByAnythingWithFilterDateIdView(generics.ListAPIView):
    """
    GET uper/search/by_anything/
    Lists all users based on a search string (not case sensitive)
    """
    permission_classes = (permissions.AllowAny,)  # Only admin can perform this operation

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

        if is_active != "''":
            print("ACTTTTTTTTTTTTTT")
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

        if start_id != "''":
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                return queryset.none()

            # Checking if the start_id <= end_id and both the ids are greater than 0
            if 0 < start_id <= end_id and end_id > 0:
                queryset = queryset.filter(id__range=(start_id, end_id))


        if start_submission != "''":
            try:
                start_submission = int(start_submission)
                end_submission = int(end_submission)
            except ValueError:
                return queryset.none()

            # Checking if the start_id <= end_id and both the ids are greater than 0
            if 0 <= start_submission <= end_submission:
                queryset = queryset.filter(submissions__range=(start_submission, end_submission))

        return queryset



"""
References:
1. https://medium.com/swlh/searching-in-django-rest-framework-45aad62e7782
2. https://stackoverflow.com/questions/25151586/django-rest-framework-retrieving-object-count-from-a-model

"""
