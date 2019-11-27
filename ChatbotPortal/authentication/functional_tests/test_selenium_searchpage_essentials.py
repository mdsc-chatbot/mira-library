"""test_selenium_searchpage_essentials.py: Search page essentials related functional testing (Regular window).
                                            It checks if search element components exists or not."""

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

import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
SEARCH_PAGE = '/chatbotportal/app/search'

WAIT_SECONDS = 3
IMPLICIT_WAIT_SECONDS = 10


class TestSearchPageEssentials(LiveServerTestCase):
    """
    This class tests for search page essential things (Not the search operation itself)
    """

    def setUp(self):
        """
        Defining the web driver.
        :return: None
        """
        self.super_user_email = 'super@test.ca'
        self.super_user_password = '12345678'
        self.regular_user_email = 'regular@test.ca'
        self.regular_user_password = '12345678'
        self.reset_db()
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(IMPLICIT_WAIT_SECONDS)

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
        self.super_user_email = 'super@test.ca'
        self.super_user_password = '12345678'
        self.regular_user_email = 'regular@test.ca'
        self.regular_user_password = '12345678'

        self.super_user = CustomUser.objects.create_superuser(
            email=self.super_user_email,
            password=self.super_user_password,
        )
        self.super_user.save()

        self.regular_user = CustomUser.objects.create_user(
            email=self.regular_user_email,
            password=self.regular_user_password,
            is_active=True
        )
        self.regular_user.save()

    @staticmethod
    def clear_db():
        """
        Clearing up the database
        :return: None
        """
        CustomUser.objects.all().delete()

    def logging_in(self, email, password):
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))

        time.sleep(WAIT_SECONDS)

        self.browser.find_element_by_name('email').send_keys(email)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

    def test_search_option_visible_to_super_user(self):
        """
        Test the admin should have the search option
        :return: None
        """
        self.logging_in(self.super_user_email, self.super_user_password)
        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)

    def test_search_option_invisible_to_regular_user(self):
        """
        Test the regular user should not have the search option
        :return: None
        """
        self.logging_in(self.regular_user_email, self.regular_user_password)

        search_option = self.browser.find_elements_by_link_text('Search')
        self.assertEqual(len(search_option), 0)

    def test_click_search_option_redirects_to_searchpage(self):
        """
        Test the admin should have the search option
        :return: None
        """
        self.logging_in(self.super_user_email, self.super_user_password)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        # Finding the id accordian
        search_accordian = self.browser.find_elements_by_class_name('title')

        self.assertURLEqual(self.live_server_url + SEARCH_PAGE, self.browser.current_url)

    def test_advanced_search_options(self):
        """
        Test the admin should have the search option
        :return: None
        """
        self.logging_in(self.super_user_email, self.super_user_password)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()
