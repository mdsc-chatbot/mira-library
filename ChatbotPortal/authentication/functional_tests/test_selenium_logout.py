"""test_selenium_logout.py: Logout related functional testing (Regular window)."""

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

LOGIN_PAGE = '/chatbotportal/app/login'
HOME_PAGE = '/chatbotportal/app'

WAIT_SECONDS = 5


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
        self.browser.implicitly_wait(WAIT_SECONDS)

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

    def logging_in(self, email=None, password=None):
        """
        This function opens the browser and finds the login related elements and perform certain actions on them.
        :param email: test user's email
        :type email: String
        :param password: test user's password
        :type password: String
        :return: A reference to a the login_button situated in the html
        :rtype: Address
        """
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))

        # Finding the email field
        email_element = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email_element)

        # Finding the password field
        password_element = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password_element)

        if email is not None:
            email_element.send_keys(email)
        if password is not None:
            password_element.send_keys(password)

        # Finding the login button
        login_button = self.browser.find_element_by_name('login_button')
        self.assertIsNotNone(login_button)

        return login_button

    def test_logout_menu_is_hidden_to_a_public_user(self):
        """
        Test public users should not be able to logout button
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, HOME_PAGE))

        # Finding the logout button
        logout_menu = self.browser.find_elements_by_link_text('Logout')
        self.assertEqual(len(logout_menu), 0)

    def test_logout_menu_is_visble_to_a_logged_in_user(self):
        """
        Test a logged in user can see the logout button
        :return: None
        """

        login_button = self.logging_in(self.active_user_email, self.active_user_password)
        login_button.click()

        # A successful login redirects to the homepage
        profile_option = self.browser.find_element_by_link_text('My Profile')
        self.assertIsNotNone(profile_option)
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

        # Login should not be visible anymore menu
        login_menu = self.browser.find_elements_by_link_text('Login')
        self.assertEqual(len(login_menu), 0)

        # Logout menu should be visible now
        logout_menu = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_menu)

    def test_logout_successfully(self):
        """
        Test a logged in user can see the logout button
        :return: None
        """

        login_button = self.logging_in(self.active_user_email, self.active_user_password)
        login_button.click()

        # A successful login redirects to the homepage
        profile_option = self.browser.find_element_by_link_text('My Profile')
        self.assertIsNotNone(profile_option)
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

        # Logout menu should be visible now
        logout_menu = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_menu)

        # Logging out
        logout_menu.click()

        # Login should be visible again
        login_menu = self.browser.find_elements_by_link_text('Login')
        self.assertEqual(len(login_menu), 1)

        # Logout should be invisible again
        logout_menu = self.browser.find_elements_by_link_text('Logout')
        self.assertEqual(len(logout_menu), 0)
