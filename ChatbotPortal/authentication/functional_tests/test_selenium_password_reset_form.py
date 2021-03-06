"""test_selenium_password_reset_form.py: Password reset form related functional testing (Regular window)."""

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
        self.browser.implicitly_wait(WAIT_SECONDS)

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

    def password_resetting(self, password1, password2):
        """
        Going to password change page and perform some actions
        :param password1: 1st password
        :param password2: confirmation field
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, PASSWORD_RESET_FORM))

        # Finding the password reset button
        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)
        self.assertFalse(password_reset_button.is_enabled())

        # Finding the new_password1 field
        password1_element = self.browser.find_element_by_name('new_password1')
        self.assertIsNotNone(password1_element)
        password1_element.send_keys(password1)

        # Finding the new_password2 field
        password2_element = self.browser.find_element_by_name('new_password2')
        self.assertIsNotNone(password2_element)
        password2_element.send_keys(password2)

        return password_reset_button

    def test_password_reset_button_is_disabled(self):
        """
        Test if password reset button is disabled if password fields do not match and are less than 8 characters
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, PASSWORD_RESET_FORM))

        # Finding the password reset button
        password_reset_button = self.browser.find_element_by_name('password_reset_button')
        self.assertIsNotNone(password_reset_button)
        self.assertFalse(password_reset_button.is_enabled())

    def test_password_reset_button_is_enabled(self):
        """
        Test if password reset button is enabled if password fields match and are al least 8 characters
        :return: None
        """
        password_reset_button = self.password_resetting(self.active_user_password, self.active_user_password)
        # The password reset button should be enabled now
        self.assertTrue(password_reset_button.is_enabled())

    def test_password_reset_button_message_for_unsuccessful_attempt(self):
        """
        Test if password reset button is enabled if password fields match and are al least 8 characters
        :return: None
        """
        password_reset_button = self.password_resetting(self.active_user_password, self.active_user_password)
        self.assertTrue(password_reset_button.is_enabled())
        password_reset_button.click()

        # Finding password reset request page button
        password_reset_request_page_button = self.browser.find_element_by_name('password_reset_request_page_button')
        self.assertIsNotNone(password_reset_request_page_button)
        self.assertEqual(password_reset_request_page_button.get_attribute('innerHTML'),
                         'Unable to reset! Please request password reset email again.')

        # Redirecting to password reset request email field
        password_reset_request_page_button.click()

        password_reset_request_page_button = self.browser.find_element_by_name('email')
        self.assertIsNotNone(password_reset_request_page_button)


"""
Note: 
Successful password reset was not tested because that requires email verification simulation. 
However, password can be reset successfully following the link send in the email address.
"""
