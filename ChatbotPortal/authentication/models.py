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
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        blank=True,
        max_length=100,
        unique=False,
    )
    affiliation = models.TextField(
        verbose_name='Reason for opening account',
        blank=True,
        max_length=500,
        unique=False,
    )

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

    def __str__(self):
        return self.email
