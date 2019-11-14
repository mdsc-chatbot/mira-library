import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

# The base url
BASE_URL = 'http://127.0.0.1:8000'

url = BASE_URL + '/chatbotportal/app/login'
homepage = BASE_URL + '/chatbotportal/app'

class TestPasswordReset(LiveServerTestCase):
    """
    This class tests for signup related matters
    """

    def setUp(self):
        """
        Defining the web driver.
        :return: None
        """
        self.active_user_email = 'test@test.ca'
        self.active_user_password = '12345678'
        self.browser = webdriver.Chrome()
        # self.setUp_db()

    def tearDown(self):
        """
        Closing the browser after every test function
        :return: None
        """
        self.browser.close()
        # self.reset_db()

    def setUp_db(self):
        """
        Setting up the database
        :return: None
        """
        # CustomUser.objects.all().delete()
        # self.active_user_email = 'test@test.ca'
        # self.active_user_password = '12345678'
        # self.active_user = CustomUser.objects.create_user(
        #     email='test@login.ca',
        #     password='12345678',
        #     is_active=True
        # )
        # self.active_user.save()

    def reset_db(self):
        """
        Resetting up the database
        :return: None
        """
        CustomUser.objects.all().delete()

    def test_login_button_is_disabled(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        # self.browser.get('%s%s' % (self.live_server_url, '/chatbotportal/app/login'))
        self.browser.get(url)
        time.sleep(1)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertFalse(login_button.is_enabled())
