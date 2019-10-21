from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from .models import User


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserCreateList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateList(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerWithToken
    permission_classes = (permissions.AllowAny,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        old_password = instance.password
        response = self.update(request, *args, **kwargs)

        password = request.data['password']
        if (password is not None) and (password != ""):
            instance.set_password(password)
        else:
            instance.set_password(old_password)

        instance.first_name = request.data['first_name']
        instance.last_name = request.data['last_name']
        instance.save()

        return response
