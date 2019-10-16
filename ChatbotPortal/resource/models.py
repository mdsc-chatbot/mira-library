from django.db import models
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator


class Resource(models.Model):

    title = models.CharField(max_length=100)
    url = models.TextField(validators=[URLValidator()])
    timestamp = models.DateTimeField(auto_now_add=True)

    created_by_user = models.CharField(max_length=100)
    usefulness_rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    user_comment = models.TextField(blank=True)
    usefulness_comment = models.TextField(blank=True)

    website_summary_metadata = models.TextField(blank=True)
    website_readtime_metadata = models.DateTimeField()
    website_metadata = models.TextField(blank=True)
    website_title = models.TextField(blank=True)

    score = models.DecimalField(max_digits=10, decimal_places=1)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
