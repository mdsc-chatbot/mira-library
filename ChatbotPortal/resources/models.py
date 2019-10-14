from django.db import models

# Create your models here.
class Tags(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)