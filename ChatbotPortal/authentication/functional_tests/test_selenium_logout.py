import time

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

    def test_logout_menu_is_hidden_to_a_public_user(self):
        """
        Test public users should not be able to logout button
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, HOME_PAGE))
        time.sleep(WAIT_SECONDS)

        # Finding the logout button
        logout_menu = self.browser.find_elements_by_link_text('Logout')
        self.assertEqual(len(logout_menu), 0)

    def test_logout_menu_is_visble_to_a_logged_in_user(self):
        """
        Test a logged in user can see the logout button
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, HOME_PAGE))
        time.sleep(WAIT_SECONDS)

        # Find the login menu
        login_menu = self.browser.find_element_by_link_text('Login')
        self.assertIsNotNone(login_menu)
        login_menu.click()

        time.sleep(WAIT_SECONDS)

        # Logging in
        self.browser.find_element_by_name('email').send_keys(self.active_user_email)
        self.browser.find_element_by_name('password').send_keys(self.active_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

        # The user is redirected to the homepage
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

        # Login should not be visible anymore menu
        login_menu = self.browser.find_elements_by_link_text('Login')
        self.assertEqual(len(login_menu), 0)

        # Logout menu should be visible now
        logout_menu = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_menu)

        time.sleep(WAIT_SECONDS)

    def test_logout_successfully(self):
        """
        Test a logged in user can see the logout button
        :return: None
        """

        self.browser.get('%s%s' % (self.live_server_url, HOME_PAGE))
        time.sleep(WAIT_SECONDS)

        # Logging in
        self.browser.find_element_by_link_text('Login').click()

        time.sleep(WAIT_SECONDS)

        # Logging in
        self.browser.find_element_by_name('email').send_keys(self.active_user_email)
        self.browser.find_element_by_name('password').send_keys(self.active_user_password)
        self.browser.find_element_by_name('login_button').click()

        time.sleep(WAIT_SECONDS)

        # The user is redirected to the homepage
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

        # Login should not be visible anymore menu
        login_menu = self.browser.find_elements_by_link_text('Login')
        self.assertEqual(len(login_menu), 0)

        # Logout menu should be visible now
        logout_menu = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_menu)

        # Logging out
        logout_menu.click()

        time.sleep(WAIT_SECONDS)

        # The user is redirected to the homepage
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

        # Logout should be invisible again
        logout_menu = self.browser.find_elements_by_link_text('Logout')
        self.assertEqual(len(logout_menu), 0)

        # Login should be visible again
        login_menu = self.browser.find_elements_by_link_text('Login')
        self.assertEqual(len(login_menu), 1)

        time.sleep(WAIT_SECONDS)
