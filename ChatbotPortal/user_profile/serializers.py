from rest_framework import serializers
from .models import Profile
from signup.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'affiliation']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'status', 'submissions', 'points']
