from django.db import models
from signup.models import User
from django.db.models.signals import post_save
# from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    ACTIVE = 1
    STAFF = 2
    ADMIN = 3
    USER_STATUS = (
        (ACTIVE, 'Newbie'),
        (STAFF, 'Expert'),
        (ADMIN, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics')
    status = models.CharField(choices=USER_STATUS, null=True, max_length=10, blank=True, default='Newbie')
    submissions = models.IntegerField(blank=True, default=0)
    points = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.user.first_name} Profile'


#
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)