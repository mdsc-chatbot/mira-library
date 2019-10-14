from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

# npm install --save-dev babel-preset-es2015 babel-preset-stage-3
# npm install --save redux redux-logger redux-persist react-redux
# npm install --save axios react-router-dom lodash