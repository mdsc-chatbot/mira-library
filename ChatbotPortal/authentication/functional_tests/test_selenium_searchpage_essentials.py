import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
SEARCH_PAGE = '/chatbotportal/app/search'

WAIT_SECONDS = 3


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

    def test_search_option_visible_to_super_user(self):
        """
        Test the admin should have the search option
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

    def test_search_option_invisible_to_regular_user(self):
        """
        Test the regular user should not have the search option
        :return: None
        """
        self.browser.get('%s%s' % (self.live_server_url, LOGIN_PAGE))
        time.sleep(WAIT_SECONDS)
        self.browser.find_element_by_name('email').send_keys(self.regular_user_email)
        self.browser.find_element_by_name('password').send_keys(self.regular_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

        search_option = self.browser.find_elements_by_link_text('Search')
        self.assertEqual(len(search_option), 0)

    def test_click_search_option_redirects_to_searchpage(self):
        """
        Test the admin should have the search option
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

        self.assertURLEqual(self.live_server_url + SEARCH_PAGE, self.browser.current_url)

    def test_advanced_search_options(self):
        """
        Test the admin should have the search option
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

        time.sleep(WAIT_SECONDS)

        self.assertURLEqual(self.live_server_url + SEARCH_PAGE, self.browser.current_url)

        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        time.sleep(WAIT_SECONDS)
