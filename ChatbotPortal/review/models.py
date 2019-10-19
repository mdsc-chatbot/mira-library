from django.db import models
from enum import Enum

# Create your models here.
class Reviews(models.Model):
    class approvalChoices(Enum):
        Approved = 'APP'
        Rejected = 'REJ'
    
    class types(Enum):
        type1 = 1
        type2 = 2

    review_id = models.PositiveIntegerField(primary_key=True)
    user_id = models.PositiveIntegerField()
    review_types = types
    default = types.type1
    approved = approvalChoices
    default = approvalChoices.Rejected
    resource_url = models.TextField()