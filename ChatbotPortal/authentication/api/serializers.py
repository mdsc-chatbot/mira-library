from rest_auth import serializers as rest_auth_serializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    A serializer class that convert the CustomUser
    model instance into a native python data type.
    """

    class Meta:
        model = CustomUser
        fields = [
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
            'points'
        ]


class CustomUserTokenSerializer(serializers.ModelSerializer):
    """
    This seializer serializes the token data
    """
    # token is defined by SerializerMethodField that automatically
    # calls 'get_token(obj)' function to set the value
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """
        This method generates JWT token using obj as a payload,
        upon being called by the SerializerMethodField
        :param obj: Passed when the serializer is called (outside of the context)
        :return: Generated Json Web Token
        """

        # Get the JWT settings, add these lines after the import/from lines
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # using drf jwt utility functions to generate a token
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    class Meta:
        model = CustomUser
        fields = [
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
            'token',
            'profile_picture',
            'submissions',
            'points'
        ]


class UserUpdateSerializer(serializers.Serializer):
    """
    This serializer will serialize the update data
    """
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    profile_picture = serializers.ImageField(required=False)

    # password = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        """
        This update definition updates the instance with the validated_data
        :param instance: CustomUser model instance
        :param validated_data: data to be updated in the instance
        :return: Updated instance
        """
        # pop the password out since we need to hash it
        # password = validated_data.pop('password')
        # update the instance with the rest of the validated data fields
        instance.__dict__.update(validated_data)
        # if password:
        #     # update password if the password field was not empty
        #     instance.set_password(password)
        # Save the updated instance
        instance.save()
        return instance


class UserUpdateByAdminSerializer(serializers.Serializer):
    """
    This serializer will serialize the update data
    """
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    profile_picture = serializers.ImageField(required=False)
    is_active = serializers.BooleanField()
    is_reviewer = serializers.BooleanField()
    is_staff = serializers.BooleanField()

    def update(self, instance, validated_data):
        """
        This update definition updates the instance with the validated_data
        :param instance: CustomUser model instance
        :param validated_data: data to be updated in the instance
        :return: Updated instance
        """
        # pop the password out since we need to hash it
        # password = validated_data.pop('password')
        # update the instance with the rest of the validated data fields
        instance.__dict__.update(validated_data)
        # if password:
        #     # update password if the password field was not empty
        #     instance.set_password(password)
        # Save the updated instance
        instance.save()
        return instance

class UserUpdateSubmissionSerializer(serializers.Serializer):
    """
    This serializer will serialize the update submission
    """

    def update(self, instance, validated_data):
        """
        This update definition updates the instance with the validated_data
        :param instance: CustomUser model instance
        :param validated_data: data to be updated in the instance
        :return: Updated instance
        """
        instance.submissions += 1
        instance.pending_submissions += 1
        instance.save()
        return instance


class UserUpdateApprovedSubmissionSerializer(serializers.Serializer):
    """
    This serializer will serialize the update submission
    """

    def update(self, instance, validated_data):
        """
        This update definition updates the instance with the validated_data
        :param instance: CustomUser model instance
        :param validated_data: data to be updated in the instance
        :return: Updated instance
        """
        instance.points += 5
        instance.approved_submissions += 1
        instance.pending_submissions -= 1
        instance.save()
        return instance


class UserUpdatePasswordSerializer(serializers.Serializer):
    """
    This serializer will serialize the update data
    """
    password = serializers.CharField(max_length=255)

    def update(self, instance, validated_data):
        """
        This update definition updates the instance with the validated_data
        :param instance: CustomUser model instance
        :param validated_data: data to be updated in the instance
        :return: Updated instance
        """
        # pop the password out since we need to hash it
        password = validated_data.pop('password')
        if password:
            # update password if the password field was not empty
            instance.set_password(password)
        # Save the updated instance
        instance.save()
        return instance


class PasswordResetSerializer(rest_auth_serializer.PasswordResetSerializer):
    """
    This overrides the default rest-auth PasswordResetSerializer. This provides
    custom email template to be sent to the user upon password reset request.
    """

    def get_email_options(self):
        """
        This function sets extra email parameter to override the default email settings.
        :return: JSON of email setting
        """
        return {
            'email_template_name': 'password_reset_email.html',
            'html_email_template_name': 'password_reset_email.html'
        }
