from django.db import models
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

class Resource(models.Model):

    title = models.CharField(max_length=100)
    url = models.TextField(validators=[URLValidator()])
    timestamp = models.DateTimeField(auto_now_add=True)

    # created_by_user = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE, # If a user is deleted should their resources also be deleted?
    # )
    user_comment = models.TextField()
    usefulness_rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    usefulness_comment = models.TextField()

    website_summary_metadata = models.TextField()
    website_readtime_metadata = models.DateTimeField()
    website_metadata = models.TextField()
    website_title = models.TextField()

    score = models.DecimalField(max_digits=10, decimal_places=1)