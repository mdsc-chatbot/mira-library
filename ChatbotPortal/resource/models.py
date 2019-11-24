from django.db import models

import urllib
import urllib.request
from bs4 import BeautifulSoup

from .validators import validate_file_size
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator


class ResourceManager(models.Manager):

    def get_soup(self, url):
        r = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        html = urllib.request.urlopen(r).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def create(self, **obj_data):

        # Get website title
        try:
            url = obj_data['url']
            soup = self.get_soup(url)
            title = soup.find('title').string
            if title:
                obj_data['title'] = title
        except Exception:
            pass

        # Get website description
        try:
            url = obj_data['url']
            soup = self.get_soup(url)
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            content = meta_tag['content']
            if title:
                obj_data['website_summary_metadata'] = content
        except Exception:
            pass

        return super().create(**obj_data)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Resource(models.Model):

    title = models.TextField(default="",blank=True, null=True)
    url = models.TextField(validators=[URLValidator()])
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=1, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attachment = models.FileField(
        blank=True, upload_to='resource_attachment/', validators=[validate_file_size])

    created_by_user = models.CharField(max_length=100, default="Unknown user",blank=True, null=True)
    created_by_user_pk = models.IntegerField(default=-1, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    score = models.DecimalField(
        max_digits=10, decimal_places=1, blank=True, null=True)

    review_status = models.CharField(
        max_length=50, default="pending", blank=True, null=True)
    website_summary_metadata = models.TextField(default="", blank=True, null=True)

    public_view_count = models.IntegerField(default=0)

    objects = ResourceManager()
