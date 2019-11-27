"""admin.py: Registers the Django backend admin related privileges."""

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


# Registering the custom user model and the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)

