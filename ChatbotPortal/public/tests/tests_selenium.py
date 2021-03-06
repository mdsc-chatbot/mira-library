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

''' 
TEST CASES:
--------------------------------------------------------------------------------------
1. SEARCH 
2. TAG FILTER
3. CATEGORY FILTER
--------------------------------------------------------------------------------------
'''

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

class TestPublicPage(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.vars = {}
        self.setup_db()
        self.total_resources = 0

        super(TestPublicPage, self).setUp()

    def setup_db(self):
        Resource.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        CustomUser.objects.all().delete()

        # Creating a user
        self.user_email = "test@gmail.com"
        self.user_password = "test"
        user = CustomUser.objects.create_user(
            email=self.user_email,
            password=self.user_password,
        )
        user.save()

        # Creating tags
        english_tag = Tag.objects.create(name='English', approved=True)
        english_tag.save()
        french_tag = Tag.objects.create(name='French', approved=True)
        french_tag.save()

        # Creating categories
        website_category = Category.objects.create(name='Website')
        website_category.save()
        pdf_category = Category.objects.create(name='PDF')
        pdf_category.save()

        # Creating resources
        # 1. Resource with english tag, website
        # 2. Resource with french tag, pdf
        # 3. Resource with no tag or categories
        resource1 = Resource.objects.create(url='https://myhealth.alberta.ca/', category=website_category, review_status='approved')
        resource2 = Resource.objects.create(url='https://www.autism.org', website_summary_metadata='ARI works to advance the understanding of autism by funding research and facilitating education on its causes and the potential treatments.', category=pdf_category, review_status='approved')
        resource3 = Resource.objects.create(url='https://www.webmd.com', review_status='approved',category=website_category,)

        resource1.save()
        resource2.save()
        resource3.save()

        # After saving, we can assign tags
        resource1.tags.add(english_tag)
        resource2.tags.add(french_tag)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestPublicPage, self).tearDown()

    def test_public(self):
        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        self.login()
        self.resource_search()
        self.resource_tag()
        self.resource_category()
    
    def login(self):
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.user_email)
        self.driver.find_element(
            By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()


    def check_search_results(self, should_find_results, should_not_find_results):
        '''
        Try to find search results elements
        all test_found_results == should_find_results
        all test_not_found_results == should_not_find_results  
        '''
        test_found_results = []
        test_not_found_results = []
        
        for search_result in should_find_results + should_not_find_results:
            try:
                self.driver.find_element(By.LINK_TEXT, search_result)
                test_found_results.append(search_result)
            except:
                test_not_found_results.append(search_result)

        # print ("invalid", test_not_found_results, should_not_find_results)
        # print ("valid", test_found_results, should_find_results)

        assert test_found_results == should_find_results
        assert test_not_found_results == should_not_find_results

    def go_to_public_resources(self):
        self.driver.find_element(By.LINK_TEXT, "My Resources").click()
        self.driver.find_element(By.LINK_TEXT, "Public Resources").click()

    def resource_search(self):
        self.go_to_public_resources()
        self.driver.find_element(By.NAME, "searchBar").send_keys("MyHealth")
        self.driver.find_element(By.NAME, "searchButton").click()

        self.check_search_results(["MyHealth.Alberta.ca"], 
        ["The Autism Research Institute | #1 Advocate for Autism Research | Home", "WebMD - Better information. Better health."])

    def resource_tag(self):
        self.go_to_public_resources()
        self.driver.find_element(By.XPATH, "//label[contains(.,'English')]").click()
        self.check_search_results(["MyHealth.Alberta.ca"], 
        ["The Autism Research Institute | #1 Advocate for Autism Research | Home", "WebMD - Better information. Better health."])

        self.go_to_public_resources()
        self.driver.find_element(By.XPATH, "//label[contains(.,'French')]").click()
        self.check_search_results(["The Autism Research Institute | #1 Advocate for Autism Research | Home"], 
        ["MyHealth.Alberta.ca", "WebMD - Better information. Better health."])

    def resource_category(self):
        self.go_to_public_resources()
        self.driver.find_element(By.XPATH, "//label[contains(.,'Website')]").click()
        self.check_search_results(["MyHealth.Alberta.ca", "WebMD - Better information. Better health."], 
        ["The Autism Research Institute | #1 Advocate for Autism Research | Home"])

        self.go_to_public_resources()
        self.driver.find_element(By.XPATH, "//label[contains(.,'PDF')]").click()
        self.check_search_results(["The Autism Research Institute | #1 Advocate for Autism Research | Home"], 
        ["MyHealth.Alberta.ca", "WebMD - Better information. Better health."])

