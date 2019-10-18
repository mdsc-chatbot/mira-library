from django.db import models
# from signup.models import User
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    USER_STATUS = (
        ('Newbie', 'Newbie'),
        ('Staff', 'Staff'),
        ('Admin', 'Admin'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics')
    status = models.CharField(choices=USER_STATUS, null=True, max_length=10, blank=True, default='Newbie')
    submissions = models.IntegerField(blank=True, default=0)
    points = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.user} Profile'

# from django.db.models.signals import post_save

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
