import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
PASSWORD_RESET_PAGE = '/chatbotportal/app/password/reset'
PASSWORD_RESET_FORM = '/chatbotportal/app/password/reset/uid/token'

WAIT_SECONDS = 3


class TestPasswordResetForm(LiveServerTestCase):
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

    def test_password_reset_button_is_disabled(self):
        """
        Test if password reset button is disabled if password fields do not match and are less than 8 characters
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, PASSWORD_RESET_FORM))
        time.sleep(WAIT_SECONDS)

        # Finding the password reset button
        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)
        self.assertFalse(password_reset_button.is_enabled())

        time.sleep(WAIT_SECONDS)

    def test_password_reset_button_is_enabled(self):
        """
        Test if password reset button is enabled if password fields match and are al least 8 characters
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, PASSWORD_RESET_FORM))
        time.sleep(WAIT_SECONDS)

        # Finding the password reset button
        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)
        self.assertFalse(password_reset_button.is_enabled())

        # Finding the new_password1 field
        password1 = self.browser.find_element_by_name('new_password1')
        self.assertIsNotNone(password1)
        password1.send_keys(self.active_user_password)

        # Finding the new_password2 field
        password2 = self.browser.find_element_by_name('new_password2')
        self.assertIsNotNone(password2)
        password2.send_keys(self.active_user_password)

        # The password reset button should be enabled now
        self.assertTrue(password_reset_button.is_enabled())

        time.sleep(WAIT_SECONDS)

    def test_password_reset_button_message_for_unsuccessful_attempt(self):
        """
        Test if password reset button is enabled if password fields match and are al least 8 characters
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, PASSWORD_RESET_FORM))
        time.sleep(WAIT_SECONDS)

        # Finding the password reset button
        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)
        self.assertFalse(password_reset_button.is_enabled())

        # Finding the new_password1 field
        password1 = self.browser.find_element_by_name('new_password1')
        self.assertIsNotNone(password1)
        password1.send_keys(self.active_user_password)

        # Finding the new_password2 field
        password2 = self.browser.find_element_by_name('new_password2')
        self.assertIsNotNone(password2)
        password2.send_keys(self.active_user_password)

        # The password reset button should be enabled now
        self.assertTrue(password_reset_button.is_enabled())
        password_reset_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding password reset request page button
        password_reset_request_page_button = self.browser.find_element_by_name('password_reset_request_page_button')
        self.assertIsNotNone(password_reset_request_page_button)
        self.assertEqual(password_reset_request_page_button.get_attribute('innerHTML'),
                         'Unable to reset! Please request password reset email again.')

        time.sleep(WAIT_SECONDS)

        # Redirecting to password reset request email field
        password_reset_request_page_button.click()

        time.sleep(WAIT_SECONDS)

        self.assertURLEqual(self.live_server_url + PASSWORD_RESET_PAGE, self.browser.current_url)

        time.sleep(WAIT_SECONDS)


"""
Note: 
Successful password reset was not tested because that requires email verification simulation. 
However, password can be reset successfully following the link send in the email address.
"""
