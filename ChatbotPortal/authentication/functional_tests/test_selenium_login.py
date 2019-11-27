import time

from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import CustomUser

LOGIN_PAGE = '/chatbotportal/app/login'
HOME_PAGE = '/chatbotportal/app'

WAIT_SECONDS = 3


class TestLogin(LiveServerTestCase):
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
        self.browser.implicitly_wait(50)

    def tearDown(self):
        """
        Closing the browser on focus after every test function
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

    def test_login_button_is_disabled(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """
        login_button = self.logging_in()
        self.assertFalse(login_button.is_enabled())

    def test_login_button_is_enabled(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """
        login_button = self.logging_in(self.active_user_email, self.active_user_password)
        self.assertTrue(login_button.is_enabled())

    def test_successful_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """
        login_button = self.logging_in(self.active_user_email, self.active_user_password)
        login_button.click()

        # A successful login redirects to the homepage
        profile_option = self.browser.find_element_by_link_text('My Profile')
        self.assertIsNotNone(profile_option)
        self.assertURLEqual(self.live_server_url + HOME_PAGE, self.browser.current_url)

    def test_unsuccessful_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """

        login_button = self.logging_in(self.active_user_email, self.active_user_password + '1234')
        self.assertTrue(login_button.is_enabled())
        login_button.click()

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')

        # Finding the inner html of the message field and check if it is equal to the intended message upon unsuccessful login
        self.assertEqual(message_field.get_attribute('innerHTML'),
                         'Incorrect Email or Password! Please try again.')
        self.assertIsNotNone(message_field)

    def test_invalid_email_attempted_login(self):
        """
        Test if the login button is disabled if both email and password fields are empty.
        :return: None
        """
        login_button = self.logging_in('InvalidEmail', self.active_user_password)
        login_button.click()

        time.sleep(WAIT_SECONDS)
