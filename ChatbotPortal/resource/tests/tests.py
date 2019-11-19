from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Resource, Category


class ResourceTest(TestCase):

    def create_resource(self, url):
        category = Category(id=1,name="website")
        resource = Resource.objects.create(
            url=url,
            category=category,
        )
        return resource

    def test_webscrape_website_title(self):
        Resource.objects.all().delete()
        resource = self.create_resource("https://myhealth.alberta.ca/")
        resource.save()
        db_resource = Resource.objects.get(pk=1)
        self.assertTrue("MyHealth.Alberta.ca" in db_resource.title.strip())

        resource = self.create_resource("https://thisisaninvalid.com/")
        resource.save()
        db_resource = Resource.objects.get(pk=1)
        self.assertTrue("" in db_resource.title.strip())

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
