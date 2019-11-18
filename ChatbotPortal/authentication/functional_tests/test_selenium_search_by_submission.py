import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ..models import CustomUser

HOME_PAGE = '/chatbotportal/app'
LOGIN_PAGE = '/chatbotportal/app/login'
SEARCH_PAGE = '/chatbotportal/app/search'

WAIT_SECONDS = 3


class TestSearchBySubmission(LiveServerTestCase):
    """
    This class tests for search by Submission related issues
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
            password=self.super_user_password
        )
        self.super_user.save()

        self.regular1_user = CustomUser.objects.create_user(
            email=self.regular1_user_email,
            password=self.regular1_user_password,
            is_active=True,
            submissions=10
        )
        self.regular1_user.save()

        self.regular2_user = CustomUser.objects.create_user(
            email=self.regular2_user_email,
            password=self.regular2_user_password,
            is_active=False,
            submissions=100
        )
        self.regular2_user.save()

        self.regular3_user = CustomUser.objects.create_user(
            email=self.regular3_user_email,
            password=self.regular3_user_password,
            is_active=True,
            is_reviewer=True,
            submissions=1000
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

    def test_search_by_submission_startSubmission_equal_endSubmission(self):
        """
        Test search by Submission range where start Submission and end Submission are the same,
        The table should return users who have submitted that many number of resources.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(100)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(100)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should not be empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_startSubmission_greater_endSubmission(self):
        """
        Test search by Submission range where start Submission greater than end Submission,
        The table should return 0 users.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(1000)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(1)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_startSubmission_less_endSubmission(self):
        """
        Test search by Submission range where start Submission less than end Submission,
        The table should return all the users up to the end range if such user exists.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(0)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(1000)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return a single user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 7)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_startSubmission_only(self):
        """
        Test search by Submission range where start Submission is only mentioned,
        The table should return 0 users.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(1)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return 0 users
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_endSubmission_only(self):
        """
        Test search by Submission range where end Submission is only mentioned,
        The table should return 0 users.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(1000)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return 0 users
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_startSubmission_and_endSubmission_are_zero(self):
        """
        Test search by Submission range where start Submission and end Submission both are zero
        The table should not be empty since 0 is a valid submission.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(0)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(0)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should not be empty
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 4)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_startSubmission_and_endSubmission_are_negatives(self):
        """
        Test search by Submission range where start Submission and end Submission both are negatives
        The table should return 0 user since Submissions must be greater than or equal to 0.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(-1)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(-1)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should return zero user
        self.assertEqual(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)

    def test_search_by_Submission_clearing_values_will_resume_regular_search(self):
        """
        Test search by Submission range where start Submission and end Submission are put and then cleared,
        The table should return search based on the remaining state.
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

        # Finding the accordian
        advanced_search_accordian = self.browser.find_element_by_id('advanced_search_accordian')
        self.assertIsNotNone(advanced_search_accordian)
        advanced_search_accordian.click()

        # Finding the date accordian
        search_accordian = self.browser.find_elements_by_class_name('title')
        self.assertEqual(search_accordian[4].get_attribute('innerText'), 'Submission range')
        search_accordian[4].click()

        time.sleep(WAIT_SECONDS)

        start_submission = self.browser.find_element_by_name('start_submission')
        self.assertIsNotNone(start_submission)
        start_submission.send_keys(1)

        end_submission = self.browser.find_element_by_name('end_submission')
        self.assertIsNotNone(end_submission)
        end_submission.send_keys(1)

        time.sleep(WAIT_SECONDS)

        # Select total option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[0].click()")

        time.sleep(WAIT_SECONDS)

        start_submission.send_keys(Keys.BACKSPACE)
        end_submission.send_keys(Keys.BACKSPACE)

        # Select reset option
        self.browser.execute_script("document.getElementsByName('submission_range_option')[3].click()")

        time.sleep(WAIT_SECONDS)

        # Finding the search button
        search_button = self.browser.find_element_by_tag_name('Button')
        self.assertIsNotNone(search_button)
        search_button.click()

        # Finding search table
        search_table = self.browser.find_element_by_class_name('ReactVirtualized__Table')
        self.assertIsNotNone(search_table)

        # Search table should not be empty
        self.assertGreater(int(search_table.get_attribute('aria-rowcount')), 0)

        time.sleep(WAIT_SECONDS)
