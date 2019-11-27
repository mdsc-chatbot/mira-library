import time
from datetime import date

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
SEARCH_PAGE = '/chatbotportal/app/search'

WAIT_SECONDS = 5
IMPLICIT_WAIT_SECONDS = 50


class TestSearchByDate(LiveServerTestCase):
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
        self.super_user_email = 'super@test.ca'
        self.super_user_password = '12345678'
        self.regular_user_email = 'regular@test.ca'
        self.regular_user_password = '12345678'

        self.super_user = CustomUser.objects.create_superuser(
            email=self.super_user_email,
            password=self.super_user_password
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

    def go_to_search_page_date_option_dropdown(self, accordion_id):
        """
        This function just goes to the search page through logging in
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))

        time.sleep(WAIT_SECONDS)

        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[0].get_attribute('innerText'), 'Date')
        search_accordian[0].click()

        # Getting the value from the drop down
        date_option_dropdown = self.browser.find_element_by_name('date_option_dropdown')
        self.assertIsNotNone(date_option_dropdown)
        date_option_dropdown.click()

        # Checking the drop down menu values
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[0],
                         'Unselected')  # Placeholder/default value
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[1], 'Unselected')  # Option 1
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[2], 'By Last Login')  # Option 2
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[3],
                         'By Creation Date')  # Option 3

        # Selecting search by last login
        date_option_dropdown.find_elements_by_class_name('text')[accordion_id].click()

    def test_advanced_search_date_by_login_date(self):
        """
        Test search by last login date
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(2)  # Choose By Last Login option

        self.browser.find_element_by_id('date_popup').click()

        # Setting up the date range
        startDate = self.browser.find_element_by_id('startDate')
        self.assertIsNotNone(startDate)
        startDate.send_keys('01/01/2019')

        endDate = self.browser.find_element_by_id('endDate')
        self.assertIsNotNone(endDate)
        endDate.send_keys('01/01/2030')

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertGreaterEqual(int(search_table.get_attribute('aria-rowcount')), 1)

    def test_advanced_search_date_by_creation_date(self):
        """
        Test search by account creation date
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(3)  # Choose By Creation Date option

        self.browser.find_element_by_id('date_popup').click()

        # Setting up the date range
        startDate = self.browser.find_element_by_id('startDate')
        self.assertIsNotNone(startDate)
        startDate.send_keys('01/01/2019')

        endDate = self.browser.find_element_by_id('endDate')
        self.assertIsNotNone(endDate)
        endDate.send_keys('01/01/2030')

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 2)

    def test_advanced_search_date_by_creation_date_without_date_range(self):
        """
        Test search by account creation date without date range input should return empty table
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(3)  # Choose By Creation Date option

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertGreaterEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_advanced_search_date_invalid_range_input_min_greater_than_max(self):
        """
        Test search by invalid date range input min > max should return empty table
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(3)  # Choose By Creation Date option

        self.browser.find_element_by_id('date_popup').click()

        # Setting up the date range
        startDate = self.browser.find_element_by_id('startDate')
        self.assertIsNotNone(startDate)
        startDate.send_keys('01/01/2019')

        endDate = self.browser.find_element_by_id('endDate')
        self.assertIsNotNone(endDate)
        endDate.send_keys(date.today().strftime('01/01/2018'))

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

    def test_advanced_search_date_option_unselected_without_date_range(self):
        """
        Test search option unselected without date range should return all the users
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(1)  # Choose Unselected

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 2)

    def test_advanced_search_date_option_unselected_with_date_range(self):
        """
        Test search option unselected with date range should return all the users
        :return: None
        """
        self.go_to_search_page_date_option_dropdown(1)  # Choose Unselected

        self.browser.find_element_by_id('date_popup').click()

        # Setting up the date range
        startDate = self.browser.find_element_by_id('startDate')
        self.assertIsNotNone(startDate)
        startDate.send_keys('01/01/2019')

        endDate = self.browser.find_element_by_id('endDate')
        self.assertIsNotNone(endDate)
        endDate.send_keys(date.today().strftime('%m/%d/%Y'))

        # Finding the search button
        search_button = self.browser.find_element_by_id('search_button')
        self.assertIsNotNone(search_button)
        search_button.click()

        time.sleep(WAIT_SECONDS)

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 2)
