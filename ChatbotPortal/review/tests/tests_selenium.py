'''
tests_selenium.py:
- test frontend selenium review submission, resource rating overwrite/review rating and review comments 
'''

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


from authentication.models import CustomUser
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import time
import sys
import os
from pathlib import Path
import textract
from resource.models import Resource, Tag
from ..models import Reviews

class TestReviewSubmission(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(4)
        self.vars = {}
        self.setup_db()
        self.total_resources = 0

        super(TestReviewSubmission, self).setUp()

    def setup_db(self):
        CustomUser.objects.all().delete()
        Resource.objects.all().delete()

        self.user_email = "test@gmail.com"
        self.user_password = "test"
        user = CustomUser.objects.create_user(
            email=self.user_email,
            password=self.user_password,
        )
        user.save()

        user = CustomUser.objects.create_user(
            email='testSubmit@test.com',
            password='12345678',
        )
        user.save()

        tagReject = Tag.objects.create(name='Poor People', approved=False)
        tagReject.save()
        tagFutureAccept = Tag.objects.create(name="Research", approved=False)
        tagFutureAccept.save()

        
        resource = Resource.objects.create(
            url = "https://www.caddra.ca/",
            rating = 4,
            comments = "ADHD resource",
            review_status = "pending",
            created_by_user='testSubmit@test.com',
            created_by_user_pk = 2,

        )
        resource.tags.add(tagReject)
        resource.tags.add(tagFutureAccept)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestReviewSubmission, self).tearDown()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_review_submission(self):

        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.user_email)
        self.driver.find_element(
            By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()

        #test accessing and viewing reviews
        self.driver.find_element(By.LINK_TEXT, "My Reviews").click()

        self.driver.find_element(By.LINK_TEXT, 'Review').click()
        #review tags
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2)").click()
        #review rating
        self.driver.find_element(By.CSS_SELECTOR, "selected:nth-child(2)").click()
        #review comments
        self.driver.find_element(By.NAME, "comments").send_keys('test comments')
        #approve review
        self.driver.find_element(By.CSS_SELECTOR, ".positive").click()

        #check results
        #open completed resources
        self.driver.find_element(By.CSS_SELECTOR, ".right:nth-child(3)").click()
        #check for approved
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .check")

        #need to check review comments

        #open review made
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1)").click()
        test_review_status = self.driver.find_element(By.ID, "review_status").text
        assert test_review_status == 'approved'

        try:
            test_tags = self.driver.find_element(
                By.XPATH, ("//div[5]")).text
            test_tags = test_tags.replace("Tags:\n", "")
            print("tags", test_tags)
        except:
            test_tags = ""
        assert test_tags == 'Research'