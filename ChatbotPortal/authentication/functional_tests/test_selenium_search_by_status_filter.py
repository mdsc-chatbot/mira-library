"""test_selenium_search_by_status_filter.py: Search by status filter related functional testing (Regular window)."""

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
IMPLICIT_WAIT_SECONDS = 50


class TestSearchByStatusFilter(LiveServerTestCase):
    """
    This class tests for search by date related issues
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
        self.regular7_user_email = 'regular7@test.ca'
        self.regular7_user_password = '12345678'

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

        self.regular7_user = CustomUser.objects.create_user(
            email=self.regular7_user_email,
            password=self.regular7_user_password,
            is_active=True,
            is_reviewer=True,
            is_staff=True
        )
        self.regular7_user.save()

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

    def opening_status_search_filter(self):
        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Status')
        search_accordian[1].click()

        time.sleep(WAIT_SECONDS)

    def test_search_status_filter_by_is_active_nonactive(self):
        """
        Test search non-active users
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up the date range
        is_active_dropdown = self.browser.find_element_by_name('is_active')
        self.assertIsNotNone(is_active_dropdown)
        is_active_dropdown.click()

        is_active_dropdown_value = is_active_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_active_dropdown_value)
        self.assertEqual(is_active_dropdown_value[2].get_attribute('innerText'), 'No')
        is_active_dropdown_value[2].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 1)

    def test_search_status_filter_by_is_reviewer_reviewer(self):
        """
        Test search reviewers
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up dropdown values
        is_reviewer_dropdown = self.browser.find_element_by_name('is_reviewer')
        self.assertIsNotNone(is_reviewer_dropdown)
        is_reviewer_dropdown.click()

        is_reviewer_dropdown_value = is_reviewer_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_reviewer_dropdown_value)
        self.assertEqual(is_reviewer_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_reviewer_dropdown_value[1].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 3)

    def test_search_status_filter_by_is_staff_nonstaff(self):
        """
        Test search users who are not staffs
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up dropdown values
        is_staff_dropdown = self.browser.find_element_by_name('is_staff')
        self.assertIsNotNone(is_staff_dropdown)
        is_staff_dropdown.click()

        is_staff_dropdown_value = is_staff_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_staff_dropdown_value)
        self.assertEqual(is_staff_dropdown_value[2].get_attribute('innerText'), 'No')
        is_staff_dropdown_value[2].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 5)

    def test_search_status_filter_by_is_active_is_reviewer_is_staff(self):
        """
        Test search a user who is active and is a reviewer and is a staff member
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up dropdown values
        is_active_dropdown = self.browser.find_element_by_name('is_active')
        self.assertIsNotNone(is_active_dropdown)
        is_active_dropdown.click()

        is_active_dropdown_value = is_active_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_active_dropdown_value)
        self.assertEqual(is_active_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_active_dropdown_value[1].click()

        # Setting up dropdown values
        is_reviewer_dropdown = self.browser.find_element_by_name('is_reviewer')
        self.assertIsNotNone(is_reviewer_dropdown)
        is_reviewer_dropdown.click()

        is_reviewer_dropdown_value = is_reviewer_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_reviewer_dropdown_value)
        self.assertEqual(is_reviewer_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_reviewer_dropdown_value[1].click()

        # Setting up dropdown values
        is_staff_dropdown = self.browser.find_element_by_name('is_staff')
        self.assertIsNotNone(is_staff_dropdown)
        is_staff_dropdown.click()

        is_staff_dropdown_value = is_staff_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_staff_dropdown_value)
        self.assertEqual(is_staff_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_staff_dropdown_value[1].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty because super user is such kind of user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 2)

    def test_search_status_filter_by_is_nonactive_is_nonreviewer_is_nonstaff(self):
        """
        Test search a user who is not active and is not a reviewer and is not a staff member
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up dropdown values
        is_active_dropdown = self.browser.find_element_by_name('is_active')
        self.assertIsNotNone(is_active_dropdown)
        is_active_dropdown.click()

        is_active_dropdown_value = is_active_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_active_dropdown_value)
        self.assertEqual(is_active_dropdown_value[2].get_attribute('innerText'), 'No')
        is_active_dropdown_value[2].click()

        # Setting up dropdown values
        is_reviewer_dropdown = self.browser.find_element_by_name('is_reviewer')
        self.assertIsNotNone(is_reviewer_dropdown)
        is_reviewer_dropdown.click()

        is_reviewer_dropdown_value = is_reviewer_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_reviewer_dropdown_value)
        self.assertEqual(is_reviewer_dropdown_value[2].get_attribute('innerText'), 'No')
        is_reviewer_dropdown_value[2].click()

        # Setting up dropdown values
        is_staff_dropdown = self.browser.find_element_by_name('is_staff')
        self.assertIsNotNone(is_staff_dropdown)
        is_staff_dropdown.click()

        is_staff_dropdown_value = is_staff_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_staff_dropdown_value)
        self.assertEqual(is_staff_dropdown_value[2].get_attribute('innerText'), 'No')
        is_staff_dropdown_value[2].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty because there is one such user: regular1
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 1)

    def test_search_status_filter_once_selected_must_be_set_to_None_to_go_back_to_normal_search(self):
        """
        Test search filters must be set to none to go back to normal search functionality
        :return: None
        """
        self.logging_in()

        self.opening_status_search_filter()

        # Setting up dropdown values
        is_active_dropdown = self.browser.find_element_by_name('is_active')
        self.assertIsNotNone(is_active_dropdown)
        is_active_dropdown.click()

        is_active_dropdown_value = is_active_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_active_dropdown_value)
        self.assertEqual(is_active_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_active_dropdown_value[1].click()

        # Setting up dropdown values
        is_reviewer_dropdown = self.browser.find_element_by_name('is_reviewer')
        self.assertIsNotNone(is_reviewer_dropdown)
        is_reviewer_dropdown.click()

        is_reviewer_dropdown_value = is_reviewer_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_reviewer_dropdown_value)
        self.assertEqual(is_reviewer_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_reviewer_dropdown_value[1].click()

        # Setting up dropdown values
        is_staff_dropdown = self.browser.find_element_by_name('is_staff')
        self.assertIsNotNone(is_staff_dropdown)
        is_staff_dropdown.click()

        is_staff_dropdown_value = is_staff_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_staff_dropdown_value)
        self.assertEqual(is_staff_dropdown_value[1].get_attribute('innerText'), 'Yes')
        is_staff_dropdown_value[1].click()

        # Clearing the selected filters to resume regular search operations

        # Setting up dropdown values
        is_active_dropdown = self.browser.find_element_by_name('is_active')
        self.assertIsNotNone(is_active_dropdown)
        is_active_dropdown.click()

        is_active_dropdown_value = is_active_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_active_dropdown_value)
        self.assertEqual(is_active_dropdown_value[3].get_attribute('innerText'), 'None')
        is_active_dropdown_value[3].click()

        # Setting up dropdown values
        is_reviewer_dropdown = self.browser.find_element_by_name('is_reviewer')
        self.assertIsNotNone(is_reviewer_dropdown)
        is_reviewer_dropdown.click()

        is_reviewer_dropdown_value = is_reviewer_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_reviewer_dropdown_value)
        self.assertEqual(is_reviewer_dropdown_value[3].get_attribute('innerText'), 'None')
        is_reviewer_dropdown_value[3].click()

        # Setting up dropdown values
        is_staff_dropdown = self.browser.find_element_by_name('is_staff')
        self.assertIsNotNone(is_staff_dropdown)
        is_staff_dropdown.click()

        is_staff_dropdown_value = is_staff_dropdown.find_elements_by_class_name('text')
        self.assertIsNotNone(is_staff_dropdown_value)
        self.assertEqual(is_staff_dropdown_value[3].get_attribute('innerText'), 'None')
        is_staff_dropdown_value[3].click()

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty and should return all the users
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 8)
