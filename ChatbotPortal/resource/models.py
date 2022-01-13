'''
models.py:
- Django models for 
1. Resource (has Resource manager to get webscraped title and description/ summary)
2. Tags
3. Category
'''

__author__ = "Apu Islam, Henry Lo, Jacy Mark, Ritvik Khanna, Yeva Nguyen"
__copyright__ = "Copyright (c) 2019 BOLDDUC LABORATORY"
__credits__ = ["Apu Islam", "Henry Lo", "Jacy Mark", "Ritvik Khanna", "Yeva Nguyen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "BOLDDUC LABORATORY"

#  MIT License
#
#  Copyright (c) 2019 BOLDDUC LABORATORY
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from enum import Enum
from django.db import models

import urllib
import urllib.request
from bs4 import BeautifulSoup

from .validators import validate_file_size
from django.core.validators import URLValidator, MaxValueValidator, MinValueValidator, RegexValidator
import ssl
import requests
from django.utils.translation import gettext as _

class ResourceManager(models.Manager):

    def get_soup(self, url):
        # r = urllib.request.Request(url, headers={
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        # html = urllib.request.urlopen(r,context=ssl.SSLContext()).read().decode('utf8')
        # Uncomment above once we have SSL figured out for deployment
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup

    def create(self, **obj_data):

        # Get website title
        # try:
        #     url = obj_data['url']
        #     soup = self.get_soup(url)
        #     title = soup.find('title').string
        #     if title:
        #         obj_data['title'] = title
        # except Exception:
        #     pass

        # Get website description
        # try:
        #     url = obj_data['url']
        #     soup = self.get_soup(url)
        #     meta_tag = soup.find('meta', attrs={'name': 'description'})
        #     content = meta_tag['content']
        #     if title:
        #         obj_data['website_summary_metadata'] = content
        # except Exception:
        #     pass

        return super().create(**obj_data)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tag_category = models.CharField(max_length = 100)
    approved = models.BooleanField(default=False)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
      

class Resource(models.Model):

    title = models.TextField(default="",blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=1, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    attachment = models.FileField(
        blank=True, upload_to='resource_attachment/', validators=[validate_file_size])
    organization_name = models.TextField(default="",blank=True, null=True)
    created_by_user = models.CharField(max_length=100, default="Unknown user",blank=True, null=True)
    created_by_user_pk = models.IntegerField(default=-1, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    score = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True)

    review_status = models.CharField(
        max_length=50, default="pending", blank=True, null=True)
    review_comments= models.TextField(
        default="No Comment", blank=True, null=True)
    assigned_reviewer = models.IntegerField(default=-1)
    review_status_2 = models.CharField(
        max_length=50, default="pending", blank=True, null=True)
    assigned_reviewer_2 = models.IntegerField(default=-1)
    website_summary_metadata = models.TextField(default="", blank=True, null=True)

    public_view_count = models.IntegerField(default=0)

    objects = ResourceManager()


    SERVICE = 'SR'#, _('Program/Service')
    RESOURCE = 'RS'#, _("Educational/Informational")
    BOTH = 'BT'#, _("Both")
    ResourceTypeEnumChoices = [
        (SERVICE, 'Program/Service'),
        (RESOURCE, 'Educational/Informational'),
        (BOTH, 'Service/Resource'),
    ]
    resource_type = models.CharField(
        max_length=2,
        choices=ResourceTypeEnumChoices,
        default="RS",
    )

    #both phone and text number fields expect the page to process the given numbers into the format "1234567890;" etc with each number ending in a semicolon
    # phone_regex = RegexValidator(regex=r'^(\d{3,15}\;)*$', message="Phone number must be entered in the format: 1234567890; , one per line. Up to 15 digits allowed per number.")
    phone_numbers = models.TextField(blank=True, null=True) # validators should be a list

    # text_regex = RegexValidator(regex=r'^(\w{3,15}\;)*$', message="Text number must be entered in the format: 1234567890; , one per line. Up to 15 digits allowed per number.")
    text_numbers = models.TextField(blank=True, null=True)

    email = models.EmailField(max_length=100, blank=True, null=True)

    index = models.TextField(blank=True, null=True)

    website_meta_data = models.TextField(blank=True, null=True)

    website_meta_data_updated_at = models.DateTimeField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    general_url = models.TextField(blank=True, null=True)

    organization_description = models.TextField(blank=True, null=True)

    #physical_address_regex = RegexValidator(regex=r'^((.)+\,)*((.{1,100}))$', message="Address format is not correct.")
    physical_address = models.TextField(blank=True, null=True)

    hours_of_operation = models.TextField(blank=True, null=True)

    definition = models.TextField(blank=True, null=True)

    max_age = models.IntegerField(
        validators=[MaxValueValidator(120), MinValueValidator(0)], default=120, blank=True, null=True)
    min_age = models.IntegerField(
        validators=[MaxValueValidator(120), MinValueValidator(0)], default=0, blank=True, null=True)

    time_zone = models.CharField(
            max_length=10,
            default="-6 UTC",
        )
