from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

# The base url
BASE_URL = 'http://127.0.0.1:8000'

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
PASSWORD_RESET_PAGE = '/chatbotportal/app/password/reset'
PASSWORD_RESET_FORM = '/chatbotportal/app/password/reset/uid/token'

WAIT_SECONDS = 3


class TestPasswordResetRequest(LiveServerTestCase):
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
        self.browser.implicitly_wait(WAIT_SECONDS)

    def tearDown(self):
        """
        Closing the browser after every test function
        :return: None
        """
        self.browser.close()

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

    def test_click_password_reset_link_on_loginpage(self):
        """
        Test if the login page can redirect to the password reset page.
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))

        # Finding the password reset link on login form
        password_reset_link = self.browser.find_element_by_id('password_reset_link')
        self.assertIsNotNone(password_reset_link)
        password_reset_link.click()

        # Check if the URL matches for the password reset page
        password_reset_request_page_button = self.browser.find_element_by_name('email')
        self.assertIsNotNone(password_reset_request_page_button)

    def test_password_reset_button_is_disabled(self):
        """
        Test if the reset button is disabled as an initial condition
        :return: None
        """

        self.test_click_password_reset_link_on_loginpage()

        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)

        # The password reset button should be disabled
        self.assertFalse(password_reset_button.is_enabled())

        return password_reset_button

    def test_email_not_sent_message(self):
        """
        Test email not sent message as the initial condition of the form
        :return: None
        """

        self.test_password_reset_button_is_disabled()

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')
        # Finding the inner html of the message field and check if it is equal to the intended message
        self.assertEqual(message_field.get_attribute('innerHTML'), 'Email is not sent yet.')
        self.assertIsNotNone(message_field)

    def test_password_reset_button_is_enabled(self):
        """
        Test if the password reset button gets enabled upon filling email field
        :return: None
        """
        password_reset_button = self.test_password_reset_button_is_disabled()

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys(self.active_user_email)

        # The password reset button should be enabled
        self.assertTrue(password_reset_button.is_enabled())

    def test_invalid_email_attempted_password_reset(self):
        """
        Test if the email field has the correct email format
        :return: None
        """

        password_reset_button = self.test_password_reset_button_is_disabled()

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys('invalidEmailFormat')

        # The password reset button should be enabled
        self.assertTrue(password_reset_button.is_enabled())
        password_reset_button.click()

    def test_successful_email_sent_message(self):
        """
        Test email not sent message as the initial condition of the form
        :return: None
        """

        password_reset_button = self.test_password_reset_button_is_disabled()

        # Finding the email field
        email = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email)
        email.send_keys(self.active_user_email)

        # The password reset button should be enabled
        self.assertTrue(password_reset_button.is_enabled())
        password_reset_button.click()

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')
        # Finding the inner html of the message field and check if it is equal to the intended message
        self.assertEqual(message_field.get_attribute('innerHTML'),
                         'An email is sent with a password change link, Please check your email.')
        self.assertIsNotNone(message_field)
