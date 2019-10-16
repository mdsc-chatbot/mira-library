from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics')
    status = models.CharField(max_length=256, blank=True, default='Newbie')
    submissions = models.IntegerField(blank=True, default=0)
    points = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.user.first_name} Profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)

# npm install --save-dev babel-preset-es2015 babel-preset-stage-3
# npm install --save redux redux-logger redux-persist react-redux
# npm install --save axios react-router-dom lodash
