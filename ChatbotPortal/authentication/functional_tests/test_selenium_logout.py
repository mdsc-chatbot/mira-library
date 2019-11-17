import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

# The base url
BASE_URL = 'http://127.0.0.1:8000'
url = BASE_URL + '/chatbotportal/app/login'
homepage = BASE_URL + '/chatbotportal/app'


class TestLogout(LiveServerTestCase):
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
        self.reset_db()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """
        Closing the browser after every test function
        :return: None
        """
        self.browser.close()
        self.clear_db()

    def reset_db(self):
        """
        Resetting up the database
        :return: None
        """
        CustomUser.objects.all().delete()
        self.active_user_email = 'test@test.ca'
        self.active_user_password = '12345678'
        self.active_user = CustomUser.objects.create_user(
            email=self.active_user_email,
            password=self.active_user_password,
            is_active=True
        )
        self.active_user.save()

    @staticmethod
    def clear_db():
        """
        Clearing up the database
        :return: None
        """
        CustomUser.objects.all().delete()

    def test_logout_is_hidden_from_not_logged_in_users(self):
        """
        Test public users should not be able to logout button
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, '/chatbotportal/app'))
        # self.browser.get(homepage)
        time.sleep(1)

        # Finding the login button
        logout_button = self.browser.find_elements_by_name('Logout')
        self.assertEqual(len(logout_button), 0)
