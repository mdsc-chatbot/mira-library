from django.db import models
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator

import urllib
import urllib.request
from bs4 import BeautifulSoup


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


class Resource(models.Model):

    title = models.TextField()
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

    objects = ResourceManager()


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
