from django.contrib.auth import authenticate, login
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .api.serializers import CustomUserSerializer, CustomUserTokenSerializer, UserUpdateSerializer
from .models import CustomUser

# from rest_framework.decorators import api_view
# from rest_framework.generics import UpdateAPIView
# from rest_framework.views import APIView
# from .serializers import UserSerializer, UserSerializerWithToken


# @api_view(['GET'])
# def current_user(request):
#     """
#     Determine the current user by their token, and return their data
#     """
#
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)
#
#
# class UserCreateList(APIView):
#     """
#     Create a new user. It's called 'UserList' because normally we'd have a get
#     method here too, for retrieving a list of all User objects.
#     """
#
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = UserSerializerWithToken(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserUpdateList(UpdateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializerWithToken
#     permission_classes = (permissions.AllowAny,)
#
#     def put(self, request, *args, **kwargs):
#         instance = self.get_object()
#         old_password = instance.password
#         response = self.update(request, *args, **kwargs)
#
#         password = request.data['password']
#         if (password is not None) and (password != ""):
#             instance.set_password(password)
#         else:
#             instance.set_password(old_password)
#
#         instance.first_name = request.data['first_name']
#         instance.last_name = request.data['last_name']
#         instance.save()
#
#         return response


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

        CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            affiliation=affiliation
        )

        return Response(status=status.HTTP_201_CREATED)


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """
    PUT auth/<pk>/update/
    Update User API
    """
    permission_classes = (permissions.IsAuthenticated,)  # Only authenticated users can update their own account
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer


class DeleteUserView(generics.DestroyAPIView):
    """
    DELETE auth/delete/<pk>/
    Delete User API
    """
    permission_classes = (permissions.IsAdminUser,)  # Only admin/super_user can delete any account
    queryset = CustomUser.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            pk = request.data.get('id', )  # getting the ID of the user to be deleted
            instance = CustomUser.objects.get(id=pk)  # getting the User from the database
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
    permission_classes = (permissions.IsAuthenticated, )    # Only authenticated users can have access
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
