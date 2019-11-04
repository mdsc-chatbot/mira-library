from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Resource


class ResourceTest(TestCase):
    def test_webscrape_website_title(self):
        Resource.objects.all().delete()
        resource = Resource.objects.create(
            title="Unknown title",
            url="https://www.ualberta.ca/",
            rating=1,
            comments="",
            created_by_user="Unknown user"
        )
        resource.save()
        db_resource = Resource.objects.get(pk=1)
        self.assertEqual(db_resource.title.strip(), "University of Alberta")

    def test_validations(self):
        Resource.objects.all().delete()
        resource = Resource.objects.create(
            title="Unknown title",
            url="https://www.ualberta.ca/",
            rating=1,
            comments="",
            created_by_user="Unknown user"
        )
        resource.full_clean()

        resource.url = "Invalid url"
        self.assertRaises(ValidationError, resource.full_clean)

        resource.rating = 10
        self.assertRaises(ValidationError, resource.full_clean)
