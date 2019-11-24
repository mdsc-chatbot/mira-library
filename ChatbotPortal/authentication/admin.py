from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin class for custom user
    """

    # Fields to be displayed
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'affiliation',
        'date_joined',
        'is_active',
        'is_reviewer',
        'is_staff',
        'is_superuser',
        'last_login',
        'profile_picture',
        'submissions',
        'pending_submissions',
        'approved_submissions',
        'points',
    ]

    # Fields to be filtered
    list_filter = [
        'date_joined',
        'is_active',
        'is_reviewer',
        'is_staff',
        'is_superuser',
        'last_login',
    ]

    # How user details would be viewed from backend admin side
    fieldsets = [
        ('Login Credentials', {'fields': ['email', 'password']}),
        ('User Details',
         {'fields': ['first_name', 'last_name', 'affiliation', 'date_joined', 'last_login',
                     'profile_picture', 'submissions', 'pending_submissions',
                     'approved_submissions', 'points']}),
        ('Permissions', {'fields': ['is_active', 'is_reviewer', 'is_staff', 'is_superuser']}),
    ]

    # Searching attributes for the admin
    search_fields = [
        'id',
        'email',
        'first_name',
        'last_name',
        'affiliation',
    ]

    # Ordering of the fields
    ordering = [
        'id',
        'email',
    ]

    filter_horizontal = ()

    # Fields that an admin can add to create a new user
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_reviewer',
                'is_active',
                'is_superuser',
                'first_name',
                'last_name',
                'affiliation',
                'profile_picture',
                'submissions',
                'pending_submissions',
                'approved_submissions',
                'points',
            )}
         ),
    ]


# Getting the user model that is active in the project
# CustomUser = get_user_model()

# Registering the custom user model and the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)

# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)
