import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ..models import CustomUser

# The base url
BASE_URL = 'http://127.0.0.1:8000'
loginpage = BASE_URL + '/chatbotportal/app/login'
homepage = BASE_URL + '/chatbotportal/app'
searchpage = BASE_URL + '/chatbotportal/app/search'


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

    def test_search_by_id_startId_equal_endId(self):
        """
        Test search by id range where start id and end id are the same,
        The table should return a single user.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 1)

        time.sleep(3)

    def test_search_by_id_startId_greater_endId(self):
        """
        Test search by id range where start id greater than end id,
        The table should return 0 users.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1000)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_startId_less_endId(self):
        """
        Test search by id range where start id less than end id,
        The table should return all the users up to the end range if such user exists.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1000)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_startId_only(self):
        """
        Test search by id range where start id is only mentioned,
        The table should return 0 users.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return 0 users
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_endId_only(self):
        """
        Test search by id range where end id is only mentioned,
        The table should return 0 users.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1000)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return 0 users
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_startId_and_endId_are_zero(self):
        """
        Test search by id range where start id and end id both are zero
        The table should return 0 user since ids must be greater than 1.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(0)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(0)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return zero user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_startId_and_endId_are_negatives(self):
        """
        Test search by id range where start id and end id both are negatives
        The table should return 0 user since ids must be greater than 1.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(-1)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(-1)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return zero user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)

    def test_search_by_id_clearing_values_will_resume_regular_search(self):
        """
        Test search by id range where start id and end id are put and then cleared,
        The table should return search based on the remaining state.
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
        self.assertEqual(search_accordian[3].get_attribute('innerText'), 'Id range')
        search_accordian[3].click()

        time.sleep(3)

        start_id = self.browser.find_element_by_name('start_id')
        self.assertIsNotNone(start_id)
        start_id.send_keys(1)

        end_id = self.browser.find_element_by_name('end_id')
        self.assertIsNotNone(end_id)
        end_id.send_keys(1)

        time.sleep(3)

        start_id.send_keys(Keys.BACKSPACE)
        end_id.send_keys(Keys.BACKSPACE)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should not be empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(3)
