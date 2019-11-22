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
        self.create_resource(url).save()
        db_resource = Resource.objects.get(pk=resource_pk)
        test_title = db_resource.title.strip()
        test_summary = db_resource.website_summary_metadata.strip()
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
