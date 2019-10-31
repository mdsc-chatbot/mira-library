from django.db import models
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

import urllib
import urllib.request
from bs4 import BeautifulSoup

from .validators import validate_file_size

class ResourceManager(models.Manager):
    def create(self, **obj_data):
        try:
            # Get website actual title
            url = obj_data['url']
            r = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            html = urllib.request.urlopen(r).read().decode('utf8')

            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title').string
            if title:
                obj_data['title'] = title

        except Exception:
            pass

        return super().create(**obj_data)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

class Resource(models.Model):

    title = models.TextField()
    url = models.TextField(validators=[URLValidator()])
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])
    comments = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    #attachment = models.FileField(blank=True, upload_to='resource_attachment/', validators=[validate_file_size(size=50)])

    created_by_user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    website_summary_metadata = models.TextField(blank=True, null=True)
    website_readtime_metadata = models.DateTimeField(blank=True, null=True)
    website_metadata = models.TextField(blank=True, null=True)
    website_title = models.TextField(blank=True, null=True)
    score = models.DecimalField(
        max_digits=10, decimal_places=1, blank=True, null=True)

    objects = ResourceManager()

