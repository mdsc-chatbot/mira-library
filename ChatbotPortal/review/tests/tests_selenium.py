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
from resource.models import Resource, Tag, Category
from ..models import Reviews

class TestReviewSubmission(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
        self.vars = {}
        self.setup_db()
        self.total_resources = 0

        super(TestReviewSubmission, self).setUp()

    def setup_db(self):
        CustomUser.objects.all().delete()
        Resource.objects.all().delete()
        Reviews.objects.all().delete()

        normal_user = CustomUser.objects.create_user(
            email='normal_user@test.com',
            password='normal_user',
        )
        reviewer_user = CustomUser.objects.create_user(
            email='reviewer_user@test.com',
            password='reviewer_user',
            is_reviewer=True,
        )
        normal_user.save()
        reviewer_user.save()

        website_category = Category.objects.create(name='Website')
        website_category.save()

        future_approved_resource = Resource.objects.create(
            url = "https://caddac.ca/adhd/resources/online-resources/",
            review_status = "pending",
            created_by_user='normal_user@test.com',
            created_by_user_pk = 1,
            category=website_category,
        )
        future_rejected_resource = Resource.objects.create(
            url = "https://www.google.ca/",
            review_status = "pending",
            created_by_user='normal_user@test.com',
            created_by_user_pk = 1,
            category=website_category,
        )
        future_approved_resource.save()
        future_rejected_resource.save()

        tag_resource = Resource.objects.create(
            url = "https://en.wikipedia.org/wiki/Attention_deficit_hyperactivity_disorder",
            review_status = "pending",
            created_by_user='normal_user@test.com',
            created_by_user_pk = 1,
            category=website_category,
        )
        future_approved_tag = Tag.objects.create(name="Research", approved=False)
        future_approved_tag.save()
        future_rejected_tag = Tag.objects.create(name='Poor People', approved=False)
        future_rejected_tag.save()
        tag_resource.tags.add(future_rejected_tag)
        tag_resource.tags.add(future_approved_tag)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestReviewSubmission, self).tearDown()

    def login(self, user_email, user_password):
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(user_email)
        self.driver.find_element(By.NAME, "password").send_keys(user_password)
        self.driver.find_element(By.NAME, "login_button").click()

    def review_a_resource(self, kwargs):
        self.driver.find_element(By.LINK_TEXT, "My Reviews").click()
        self.driver.find_element(By.XPATH, "(//a[contains(text(),'Review')])[2]").click()
        self.driver.find_element(By.NAME, "comments").clear()
        self.driver.find_element(By.NAME, "comments").send_keys(kwargs["review_comment"])
        self.driver.find_element(By.XPATH, "//div[3]/div/div/div/div/i[4]").click()
        if "review_tag" in kwargs and kwargs["review_tag"]:
            self.driver.find_element(By.CSS_SELECTOR, "label").click()
        self.driver.find_element(By.NAME, kwargs["review_status"]).click()

    def reviewer_user_process(self):
        self.login("reviewer_user@test.com", "reviewer_user")
        self.review_a_resource(
            {
            "review_item_xpath":"//a[contains(@href, \'/chatbotportal/app/review/3\')]",
            "review_comment":"wikipedia resource is approved.",
            "review_status":"approve",
            "review_tag":True
            }
        )
        self.review_a_resource(
            {
            "review_item_xpath":"//a[contains(@href, \'/chatbotportal/app/review/2\')]",
            "review_comment":"https://www.google.ca/ resource is rejected.",
            "review_status":"reject",
            }
        )
        self.review_a_resource(
            {
            "review_item_xpath":"//a[contains(@href, \'/chatbotportal/app/review/1\')]",
            "review_comment":"https://caddac.ca/adhd/resources/online-resources/ resource is approved.",
            "review_status":"approve",
            }
        )
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def check_resource_review_status(self, kwargs):
        self.driver.find_element(By.LINK_TEXT, "My Resources").click()
        self.driver.find_element(By.XPATH, (kwargs["resource_xpath"])).click()
        test_review_status = self.driver.find_element(By.ID, "review_status").text
        test_review_comment = self.driver.find_element(By.ID, "review_comment").text
        assert test_review_status == kwargs["review_status"]
        print("review", test_review_comment,kwargs["review_comment"])
        assert test_review_comment == kwargs["review_comment"]

        # This resource has approved and rejected tags
        if "review_tag" in kwargs and kwargs["review_tag"]:
            test_tags = self.driver.find_element(
                By.XPATH, ("//div[5]")).text
            test_tags = test_tags.replace("Tags:\n", "")
            print("test tags", test_tags)
            assert test_tags == "Research"

    def normal_user_process(self):
        self.login("normal_user@test.com", "normal_user")
        self.check_resource_review_status(
            {
            "resource_xpath":"//a[1]/div/div",
            "review_status":"approved",
            "review_comment":"https://caddac.ca/adhd/resources/online-resources/ resource is approved.",
            }
        )
        self.check_resource_review_status(
            {
            "resource_xpath":"//a[2]/div/div",
            "review_status":"rejected",
            "review_comment":"https://www.google.ca/ resource is rejected.",
            }
        )
        self.check_resource_review_status(
            {
            "resource_xpath":"//a[3]/div/div",
            "review_status":"approved",
            "review_comment":"wikipedia resource is approved.",
            "review_tag":True,
            }
        )

    def public_resource_process(self):

        # Should not find rejected resource
        try:
            self.driver.find_element(By.LINK_TEXT, "Google")
            assert False
        except:
            assert True

        for resource_link_text in ["Online Resources - Centre for ADHD Awareness Canada", "Attention deficit hyperactivity disorder - Wikipedia"]:
            # Public resources should not have review_comment
            self.driver.find_element(By.LINK_TEXT, "Public Resources").click()
            self.driver.find_element(By.LINK_TEXT, resource_link_text).click()
            try:
                self.driver.find_element(By.ID, "review_comment")
                assert False
            except:
                assert True

    def test_review_submission(self):

        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        self.reviewer_user_process()
        self.normal_user_process()
        self.public_resource_process()

        
