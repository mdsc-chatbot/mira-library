from django.db import models
from enum import Enum

# Create your models here.
class Reviews(models.Model):

    reviewer_user_email = models.CharField(max_length=100)
    approved = models.BooleanField()
    resource_url = models.TextField()
    resource_id = models.PositiveIntegerField()