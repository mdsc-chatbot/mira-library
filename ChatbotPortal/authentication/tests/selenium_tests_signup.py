import time

from django.test import LiveServerTestCase
from selenium import webdriver

# The base url
from ..models import CustomUser

BASE_URL = 'http://127.0.0.1:8000'

url = BASE_URL + '/chatbotportal/app/login'

validate_email_url = BASE_URL + '/chatbotportal/app/validate/email'


class TestSignup(LiveServerTestCase):
    """
    This class tests for signup related matters
    """

    def setUp(self):
        """
        Defining the web driver.
        :return: None
        """
        self.browser = webdriver.Chrome()
        CustomUser.objects.all().delete()

    def tearDown(self):
        """
        Closing the browser after every test function
        :return: None
        """
        self.browser.close()

    def test_signup_new_user(self):
        """
        Testing for successful signing up of a new user
        :return: None
        """
        # self.browser.get('%s%s' % (self.live_server_url, '/chatbotportal/app/login'))
        self.browser.get(url)
        time.sleep(1)

        # Finding the signup link on login form
        signup_link = self.browser.find_element_by_id('signup_link')
        self.assertIsNotNone(signup_link)

        signup_link.click()

        # Finding the submit button
        submit_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(submit_button)

        # Checking if the button field is active,
        # but the button field will only get active
        # if both email field is filled, and password fields matches with at most 8 characters
        self.assertFalse(submit_button.is_enabled())

        # Finding the first name field
        first_name_field = self.browser.find_element_by_name('first_name')
        self.assertIsNotNone(first_name_field)
        first_name_field.send_keys('Testing')

        # Finding the last name field
        last_name_field = self.browser.find_element_by_name('last_name')
        self.assertIsNotNone(last_name_field)
        last_name_field.send_keys('Signup')

        # Finding the email field
        email_field = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email_field)
        email_field.send_keys('test@test.ca')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the affiliation field
        affiliation_field = self.browser.find_element_by_name('affiliation')
        self.assertIsNotNone(affiliation_field)
        affiliation_field.send_keys('Testing signing up as a new user')

        # Finding the password field
        password_field = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password_field)
        password_field.send_keys('12345678')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the password confirm field
        password_confirm_field = self.browser.find_element_by_name('password2')
        self.assertIsNotNone(password_confirm_field)
        password_confirm_field.send_keys('12345678')

        # Checking if the button is active
        self.assertTrue(submit_button.is_enabled())
        submit_button.click()

        # Waiting until next page gets loaded
        time.sleep(5)

        # Checking the url of the next page
        self.assertURLEqual(self.browser.current_url, validate_email_url)

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')

        # Finding the inner html of the message field and check if it is equal to the intended message
        self.assertEqual(message_field.get_attribute('innerHTML'),
                         'An activation email has been sent to your email address. Please check your email. Thank you!')
        self.assertIsNotNone(message_field)

        # Waiting for tester's experience
        time.sleep(1)

    def test_signup_existing_user(self):
        """
        Testing for signing up a user with an existing email address
        :return: None
        """
        # self.browser.get('%s%s' % (self.live_server_url, '/chatbotportal/app/login'))
        self.browser.get(url)
        time.sleep(1)

        # Finding the signup link on login form
        signup_link = self.browser.find_element_by_id('signup_link')
        self.assertIsNotNone(signup_link)

        signup_link.click()

        # Finding the submit button
        submit_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(submit_button)

        # Checking if the button field is active,
        # but the button field will only get active
        # if both email field is filled, and password fields matches with at most 8 characters
        self.assertFalse(submit_button.is_enabled())

        # Finding the first name field
        first_name_field = self.browser.find_element_by_name('first_name')
        self.assertIsNotNone(first_name_field)
        first_name_field.send_keys('Testing')

        # Finding the last name field
        last_name_field = self.browser.find_element_by_name('last_name')
        self.assertIsNotNone(last_name_field)
        last_name_field.send_keys('Signup')

        # Finding the email field
        email_field = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email_field)
        email_field.send_keys('test@test.ca')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the affiliation field
        affiliation_field = self.browser.find_element_by_name('affiliation')
        self.assertIsNotNone(affiliation_field)
        affiliation_field.send_keys('Testing signing up as a new user')

        # Finding the password field
        password_field = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password_field)
        password_field.send_keys('12345678')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the password confirm field
        password_confirm_field = self.browser.find_element_by_name('password2')
        self.assertIsNotNone(password_confirm_field)
        password_confirm_field.send_keys('12345678')

        # Checking if the button is active
        self.assertTrue(submit_button.is_enabled())
        submit_button.click()

        # Waiting until next page gets loaded
        time.sleep(5)

        # Find the message field for the next page
        message_field = self.browser.find_element_by_tag_name('p')

        # Finding the inner html of the message field and check if it is equal to the intended message
        self.assertEqual(message_field.get_attribute('innerHTML'),
                         'Email already exists. Please try a new email address.')
        self.assertIsNotNone(message_field)

        # Waiting for tester's experience
        time.sleep(1)

    def test_signup_with_invalid_email(self):
        """
        Testing for signing up of a user with invalid email address
        :return: None
        """
        # self.browser.get('%s%s' % (self.live_server_url, '/chatbotportal/app/login'))
        self.browser.get(url)
        time.sleep(1)

        # Finding the signup link on login form
        signup_link = self.browser.find_element_by_id('signup_link')
        self.assertIsNotNone(signup_link)

        signup_link.click()

        # Finding the submit button
        submit_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(submit_button)

        # Checking if the button field is active,
        # but the button field will only get active
        # if both email field is filled, and password fields matches with at most 8 characters
        self.assertFalse(submit_button.is_enabled())

        # Finding the first name field
        first_name_field = self.browser.find_element_by_name('first_name')
        self.assertIsNotNone(first_name_field)
        first_name_field.send_keys('Testing')

        # Finding the last name field
        last_name_field = self.browser.find_element_by_name('last_name')
        self.assertIsNotNone(last_name_field)
        last_name_field.send_keys('Signup')

        # Finding the email field
        email_field = self.browser.find_element_by_name('email')
        self.assertIsNotNone(email_field)
        email_field.send_keys('testtestca')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the affiliation field
        affiliation_field = self.browser.find_element_by_name('affiliation')
        self.assertIsNotNone(affiliation_field)
        affiliation_field.send_keys('Testing signing up as a new user')

        # Finding the password field
        password_field = self.browser.find_element_by_name('password')
        self.assertIsNotNone(password_field)
        password_field.send_keys('12345678')

        # Checking if the button field is active
        self.assertFalse(submit_button.is_enabled())

        # Finding the password confirm field
        password_confirm_field = self.browser.find_element_by_name('password2')
        self.assertIsNotNone(password_confirm_field)
        password_confirm_field.send_keys('12345678')

        # Checking if the button is active
        self.assertTrue(submit_button.is_enabled())
        submit_button.click()

        # Waiting until next page gets loaded
        time.sleep(1)
