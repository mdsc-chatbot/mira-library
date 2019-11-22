import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

LOGIN_PAGE = '/chatbotportal/app/login'
HOME_PAGE = '/chatbotportal/app'

WAIT_SECONDS = 5


class TestLogin(LiveServerTestCase):
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
        Closing the browser on focus after every test function
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

    def test_login_button_is_disabled(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertFalse(login_button.is_enabled())

    def test_login_button_is_enabled(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys(self.active_user_email)

        # Finding the password field
        password = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password)
        password.send_keys(self.active_user_password)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertTrue(login_button.is_enabled())

    def test_successful_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys(self.active_user_email)

        time.sleep(WAIT_SECONDS)

        # Finding the password field
        password = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password)
        password.send_keys(self.active_user_password)

        time.sleep(WAIT_SECONDS)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertTrue(login_button.is_enabled())
        login_button.click()

        time.sleep(WAIT_SECONDS)

        # A successful login redirects to the homepage
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

    def test_unsuccessful_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys(self.active_user_email)

        time.sleep(WAIT_SECONDS)

        # Finding the password field
        password = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password)
        password.send_keys(self.active_user_password + '1234')

        time.sleep(WAIT_SECONDS)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertTrue(login_button.is_enabled())
        login_button.click()

        time.sleep(WAIT_SECONDS)

        # A successful login redirects to the homepage
        self.assertURLEqual(self.live_server_url + LOGIN_PAGE, self.browser.current_url)

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')

        # Finding the inner html of the message field and check if it is equal to the intended message upon unsuccessful login
        self.assertEqual(message_field.get_attribute('innerHTML'),
                         'Incorrect Email or Password! Please try again.')
        self.assertIsNotNone(message_field)

    def test_invalid_email_attempted_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys('InvalidEmail')

        time.sleep(WAIT_SECONDS)

        # Finding the password field
        password = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password)
        password.send_keys(self.active_user_password)

        time.sleep(WAIT_SECONDS)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)
        self.assertTrue(login_button.is_enabled())
        login_button.click()

        time.sleep(WAIT_SECONDS)
