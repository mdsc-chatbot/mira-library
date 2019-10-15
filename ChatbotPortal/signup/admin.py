from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from signup.forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User


# Register your models here.

class UserAdmin(BaseUserAdmin):
    # # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definition on the base user admin
    # that reference specific fields on auth.User.

    list_display = ('email', 'first_name', 'last_name','admin', 'staff')
    list_filter = ('admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


User = get_user_model()
admin.site.register(User, UserAdmin)
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
