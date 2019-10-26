from rest_framework import serializers

from authentication.api.serializers import CustomUserSerializer
from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'status', 'submissions', 'points']
