"""test_selenium_search_by_id.py: Search by id related functional testing (Regular window)."""

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
from selenium.webdriver.common.keys import Keys

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
SEARCH_PAGE = '/chatbotportal/app/search'

WAIT_SECONDS = 3
IMPLICIT_WAIT_SECONDS = 50


class TestSearchById(LiveServerTestCase):
    """
    This class tests for search by id related issues
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
        self.regular1_user_email = 'regular1@test.ca'
        self.regular1_user_password = '12345678'
        self.regular2_user_email = 'regular2@test.ca'
        self.regular2_user_password = '12345678'
        self.regular3_user_email = 'regular3@test.ca'
        self.regular3_user_password = '12345678'
        self.regular4_user_email = 'regular4@test.ca'
        self.regular4_user_password = '12345678'
        self.regular5_user_email = 'regular5@test.ca'
        self.regular5_user_password = '12345678'
        self.regular6_user_email = 'regular6@test.ca'
        self.regular6_user_password = '12345678'

        self.super_user = CustomUser.objects.create_superuser(
            email=self.super_user_email,
            password=self.super_user_password,
        )
        self.super_user.save()

        self.regular1_user = CustomUser.objects.create_user(
            email=self.regular1_user_email,
            password=self.regular1_user_password,
            is_active=True
        )
        self.regular1_user.save()

        self.regular2_user = CustomUser.objects.create_user(
            email=self.regular2_user_email,
            password=self.regular2_user_password,
            is_active=False
        )
        self.regular2_user.save()

        self.regular3_user = CustomUser.objects.create_user(
            email=self.regular3_user_email,
            password=self.regular3_user_password,
            is_active=True,
            is_reviewer=True
        )
        self.regular3_user.save()

        self.regular4_user = CustomUser.objects.create_user(
            email=self.regular4_user_email,
            password=self.regular4_user_password,
            is_active=True,
            is_reviewer=False
        )
        self.regular4_user.save()

        self.regular5_user = CustomUser.objects.create_user(
            email=self.regular5_user_email,
            password=self.regular5_user_password,
            is_active=True,
            is_reviewer=False,
            is_staff=True
        )
        self.regular5_user.save()

        self.regular6_user = CustomUser.objects.create_user(
            email=self.regular6_user_email,
            password=self.regular6_user_password,
            is_active=True,
            is_reviewer=False,
            is_staff=False
        )
        self.regular6_user.save()

    @staticmethod
    def clear_db():
        """
        Clearing up the database
        :return: None
        """
        CustomUser.objects.all().delete()

    def logging_in(self):
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))

        time.sleep(WAIT_SECONDS)

        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

    def search_by_id_range(self, id1=None, id2=None):
        """
        This function executes the search by setting appropriate ids
        :param id1: start id
        :param id2: end id
        :return: None
        """
        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        self.assertURLEqual(self.live_server_url + SEARCH_PAGE, self.browser.current_url)

        # Finding the id accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[2].get_attribute('innerText'), 'By Id')
        search_accordian[2].click()

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)

        if id1 is not None:
            start_id.send_keys(id1)
        if id2 is not None:
            end_id.send_keys(id2)

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

    def test_search_by_id_startId_equal_endId(self):
        """
        Test search by id range where start id and end id are the same,
        The table should return a single user.
        :return: None
        """
        self.logging_in()

        user = CustomUser.objects.get(email=self.super_user_email)

        self.search_by_id_range(user.id, user.id)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 1)

    def test_search_by_id_startId_greater_endId(self):
        """
        Test search by id range where start id greater than end id,
        The table should return 0 users.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(1000, 1)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_search_by_id_startId_less_endId(self):
        """
        Test search by id range where start id less than end id,
        The table should return all the users up to the end range if such user exists.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(1, 1000)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 7)

    def test_search_by_id_startId_only(self):
        """
        Test search by id range where start id is only mentioned,
        The table should return 0 users.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(id1=1)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_search_by_id_endId_only(self):
        """
        Test search by id range where end id is only mentioned,
        The table should return 0 users.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(id2=1000)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_search_by_id_startId_and_endId_are_zero(self):
        """
        Test search by id range where start id and end id both are zero
        The table should return 0 user since ids must be greater than 1.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(0, 0)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_search_by_id_startId_and_endId_are_negatives(self):
        """
        Test search by id range where start id and end id both are negatives
        The table should return 0 user since ids must be greater than 1.
        :return: None
        """
        self.logging_in()

        self.search_by_id_range(-1, -1)

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_search_by_id_clearing_values_will_resume_regular_search(self):
        """
        Test search by id range where start id and end id are put and then cleared,
        The table should return search based on the remaining state.
        :return: None
        """
        self.logging_in()

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        self.assertURLEqual(self.live_server_url + SEARCH_PAGE, self.browser.current_url)

        # Finding the id accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[2].get_attribute('innerText'), 'By Id')
        search_accordian[2].click()

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1)

        start_id.send_keys(Keys.BACKSPACE)
        end_id.send_keys(Keys.BACKSPACE)

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should not be empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)
