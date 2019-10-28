from django.contrib import admin
from .models import Profile


# Register your models here.
# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # fields = ['user', 'profile_picture']
    list_display = ['user', 'profile_picture', 'status', 'submissions', 'points']
