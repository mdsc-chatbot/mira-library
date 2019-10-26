from rest_framework import serializers
from .models import Profile
from authentication.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'status', 'submissions', 'points']
