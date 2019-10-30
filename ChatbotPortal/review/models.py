from django.db import models
from enum import Enum
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Reviews(models.Model):

    reviewer_user_email = models.CharField(max_length=100)
    approved = models.BooleanField()
    resource_url = models.TextField()
    resource_id = models.PositiveIntegerField()
    #review_comments = models.TextField()
    #review_rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])