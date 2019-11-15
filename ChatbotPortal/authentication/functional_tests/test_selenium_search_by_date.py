import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

# The base url
BASE_URL = 'http://127.0.0.1:8000'
loginpage = BASE_URL + '/chatbotportal/app/login'
homepage = BASE_URL + '/chatbotportal/app'
searchpage = BASE_URL + '/chatbotportal/app/search'


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
        # self.reset_db()
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """
        Closing the browser after every test function
        :return: None
        """
        self.browser.close()
        # self.clear_db()

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

    def test_advanced_search_date_by_login_date(self):
        """
        Test search by last login date
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

        # Setting up the date range
        date_range = self.browser.find_element_by_name('datesRange')
        self.assertIsNotNone(date_range)
        date_range.send_keys('2019-01-01 - 2022-01-01')

        # Getting the value from the drop down
        date_option_dropdown = self.browser.find_element_by_name('date_option_dropdown')
        self.assertIsNotNone(date_option_dropdown)
        date_option_dropdown.click()

        # Checking the drop down menu values
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[0], 'Unselected') # Placeholder/default value
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[1], 'Unselected') # Option 1
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[2], 'By Last Login') # Option 2
        self.assertEqual(date_option_dropdown.get_attribute('innerText').splitlines()[3], 'By Creation Date') # Option 3

        # Selecting search by last login
        date_option_dropdown.find_elements_by_class_name('text')[2].click() # Select 'By Last Login'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_advanced_search_date_by_creation_date(self):
        """
        Test search by account creation date
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

        # Setting up the date range
        date_range = self.browser.find_element_by_name('datesRange')
        self.assertIsNotNone(date_range)
        date_range.click()
        date_range.send_keys('2019-01-01 - 2022-01-01')

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[3].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_advanced_search_date_by_creation_date_without_date_range(self):
        """
        Test search by account creation date without date range input should return empty table
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[3].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_advanced_search_date_invalid_range_input_min_greater_than_max(self):
        """
        Test search by invalid date range input min > max should return empty table
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

        # Setting up the date range
        date_range = self.browser.find_element_by_name('datesRange')
        self.assertIsNotNone(date_range)
        date_range.click()
        self.browser.find_element_by_css_selector("tr:nth-child(5) > td:nth-child(7)").click()
        self.browser.find_element_by_css_selector("tr:nth-child(1) > td:nth-child(6) > .suicr-content-item").click()

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[3].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_advanced_search_date_range_not_selected(self):
        """
        Test search without date range should return empty table
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[3].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_advanced_search_date_option_unselected_without_date_range(self):
        """
        Test search option unselected without date range should return all the users
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[1].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertGreaterEqual(int(search_table.get_attribute('aria-rowcount')), CustomUser.objects.count())

        time.sleep(3)

    def test_advanced_search_date_option_unselected_with_date_range(self):
        """
        Test search option unselected with date range should return all the users
        :return: None
        """
        self.browser.get(loginpage)
        self.browser.find_element_by_name('email').send_keys(self.super_user_email)
        self.browser.find_element_by_name('password').send_keys(self.super_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(3)

        search_option = self.browser.find_element_by_link_text('Search')
        self.assertIsNotNone(search_option)
        search_option.click()

        time.sleep(3)

        self.assertURLEqual(self.browser.current_url, searchpage)

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[1].get_attribute('innerText'), 'Date')
        search_accordian[1].click()

        time.sleep(3)

        # Setting up the date range
        date_range = self.browser.find_element_by_name('datesRange')
        self.assertIsNotNone(date_range)
        date_range.click()
        date_range.send_keys('2019-01-01 - 2022-01-01')

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

        # Selecting search by creation date
        date_option_dropdown.find_elements_by_class_name('text')[1].click()  # Select 'By Creation Date'

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table is not empty
        self.assertGreaterEqual(int(search_table.get_attribute('aria-rowcount')), CustomUser.objects.count())

        time.sleep(3)