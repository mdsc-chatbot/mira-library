"""test_selenium_profile.py: Profile related functional testing (Regular window)."""

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
        
    def test_reset_password(self):
        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        self.login()
        self.driver.find_element(By.LINK_TEXT, "My Profile").click()
        self.driver.find_element(By.NAME, "change_password").click()
        self.user_password = "newpasswordtest"
        self.driver.find_element(By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "new_password2").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        self.login()
        self.driver.find_element(By.LINK_TEXT, "My Profile").click()
        test_user_email = self.driver.find_element(By.ID, "email").text
        assert self.user_email == test_user_email