from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.current_user_url = reverse('current_user')
        self.user_create_list_url = reverse('user_create_list')
        self.update_user_url = reverse('user_update', args=['2'])
        self.u1 = User.objects.create(
            first_name = 'TestView',
            last_name = 'TestView',
            email = 'test@test.ca',
            password = '1234'
        )

    def test_current_user_GET(self):
        response = self.client.get(self.current_user_url)

        self.assertEquals(response.status_code, 401)

    def test_create_user(self):
        response = self.client.post(self.user_create_list_url, {
            'first_name': 'NEWTESTUSER',
            'last_name': 'newtestuser',
            'email': 'newtest@newtest.ca',
            'password': '1234'
        })

        user = User.objects.get(email='newtest@newtest.ca')
        self.assertEquals(user.first_name, 'NEWTESTUSER')

    def test_update_user(self):
        response = self.client.put(self.update_user_url, {
            'first_name' : 'TestView',
            'last_name' : 'TestView',
            'email' : 'test@test.ca',
            'password' : '1234'
        })
        user = User.objects.get(id=1)
        self.assertEquals(user.email, 'test@test.ca')
        self.assertEquals(user.first_name, 'TestView')
        self.assertEquals(user.last_name, 'TestView')