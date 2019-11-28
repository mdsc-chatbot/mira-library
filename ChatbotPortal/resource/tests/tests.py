'''
test.py:
- test backend Django webscraping for :
1. resource title and description (summary)
2. url and ratings validations

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

from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Resource, Category


class ResourceTest(TestCase):

    def create_resource(self, url, rating=1):
        category = Category(id=1,name="website")
        resource = Resource.objects.create(
            url=url,
            category=category,
            rating=rating,
        )
        return resource

    def compare_resource_webscraped(self, resource_pk, url, title, summary):
        resource = self.create_resource(url)
        resource.save()

        test_title = resource.title.strip()
        test_summary = resource.website_summary_metadata.strip()
        # print("title:", test_title, "summary:", test_summary )
        self.assertTrue(title == test_title and summary == test_summary)

    def test_webscrape_website_title(self):
        Resource.objects.all().delete()

        self.compare_resource_webscraped(1,"https://myhealth.alberta.ca/", "MyHealth.Alberta.ca", "")

        self.compare_resource_webscraped(2,"https://thisisaninvalid.com/", "", "")

        self.compare_resource_webscraped(
            3, "https://caddac.ca/adhd/resources/online-resources/", 
            "Online Resources - Centre for ADHD Awareness Canada", 
            "list of canadian and international online resources adhd")

    def test_validations(self):
        Resource.objects.all().delete()
        resource = self.create_resource("https://myhealth.alberta.ca/")
        resource.full_clean()

        resource.url = "this_is_an_invalid_url"
        self.assertRaises(ValidationError, resource.full_clean)

        resource.url = "www.thisisaninvalidurl.com"
        self.assertRaises(ValidationError, resource.full_clean)

        resource.rating = 10
        self.assertRaises(ValidationError, resource.full_clean)
    
    def test_ratings(self):
        Resource.objects.all().delete()
        resource = self.create_resource("https://www.caddra.ca/", rating=4)
        db_resource = Resource.objects.get(pk=1)
        self.assertTrue(4==db_resource.rating)
