"""models.py: Defines the CustomUser model that would be used throughout the project."""

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

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that will help defining custom user fields
    """
    email = models.EmailField(
        verbose_name='Email Address',
        blank=False,
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='First Name',
        blank=True,
        max_length=100,
        unique=False,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        blank=True,
        max_length=100,
        unique=False,
        null=True,
    )
    affiliation = models.TextField(
        verbose_name='Reason for opening account',
        blank=True,
        max_length=500,
        unique=False,
        null=True,
    )

    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_pics')

    submissions = models.IntegerField(blank=True, default=0)
    pending_submissions = models.IntegerField(blank=True, default=0)
    approved_submissions = models.IntegerField(blank=True, default=0)

    points = models.IntegerField(blank=True, default=0)

    date_joined = models.DateTimeField(default=timezone.now)

    # Will be turned into True after email verification
    is_active = models.BooleanField(default=True)

    # The newly created user by default is not a reviewer
    is_reviewer = models.BooleanField(default=False)

    # A user; with more rights than regular users
    is_staff = models.BooleanField(default=False)

    # A superuser; with all rights
    is_superuser = models.BooleanField(default=False)

    # notice the absence of a "Password field", that's built in.

    # Email would be used instead of username
    USERNAME_FIELD = 'email'

    # Email & Password are required by default.
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # def __str__(self):
    #     return self.first_name
