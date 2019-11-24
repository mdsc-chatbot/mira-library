# Generated by Selenium IDE
from authentication.models import CustomUser
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from ..models import CustomUser


class TestProfile(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(50)
        self.setup_db()

        super(TestProfile, self).setUp()

    def setup_db(self):
        CustomUser.objects.all().delete()

        self.user_email = "test@gmail.com"
        self.user_password = "test"
        user = CustomUser.objects.create_user(
            email=self.user_email,
            password=self.user_password,
        )
        user.save()

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestProfile, self).tearDown()

    def test_profile(self):

        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        save_changes_test_kwargs = {
            "input_first_name":"Test",
            "input_last_name":"Profile",
            "expected_first_name":"Test",
            "expected_last_name":"Profile",
            "test_first_name":"",
            "test_last_name":"",
            "option":"save",
        }
        self.profile_test(save_changes_test_kwargs)
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        not_save_changes_test_kwargs = {
            "input_first_name": "New_Test",
            "input_last_name": "New_Profile",
            "expected_first_name": "Test",
            "expected_last_name": "Profile",
            "test_first_name": "",
            "test_last_name": "",
            "option": "cancel",
        }
        self.profile_test(not_save_changes_test_kwargs)

    def profile_test(self, kwargs):

        self.login()
        self.edit_profile(kwargs)
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        self.login()
        self.get_profile(kwargs)
        self.compare_profile(kwargs)
        
    def login(self):
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.user_email)
        self.driver.find_element(
            By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()

    def edit_profile(self, kwargs):
        self.driver.find_element(By.LINK_TEXT, "My Profile").click()
        self.driver.find_element(
            By.NAME, "first_name").clear()
        self.driver.find_element(
            By.NAME, "first_name").send_keys(kwargs["input_first_name"])
        self.driver.find_element(
            By.NAME, "last_name").clear()
        self.driver.find_element(
            By.NAME, "last_name").send_keys(kwargs["input_last_name"])
        if kwargs["option"] == "save":
            self.driver.find_element(
                By.NAME, kwargs["option"]).click()
            time.sleep(1)
        else:
            # since cancel button will be remove, canceling changes will just be switching to another page
            self.driver.find_element(By.LINK_TEXT, "Public Resources").click() 
        

    def get_profile(self, kwargs):
        self.driver.find_element(By.LINK_TEXT, "My Profile").click()
        kwargs["test_first_name"] = self.driver.find_element(
            By.NAME, "first_name").get_attribute("value")
        kwargs["test_last_name"] = self.driver.find_element(
            By.NAME, "last_name").get_attribute("value")
        
    def compare_profile(self, kwargs):
        assert kwargs["expected_first_name"] == kwargs["test_first_name"]
        assert kwargs["expected_last_name"] == kwargs["test_last_name"]
        
