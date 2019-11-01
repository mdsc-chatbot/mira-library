
''' 
TEST CASES:

1 Resource submission basic: only url and resource rating
INPUT
- url: https://www.google.com/
- resource rating: 2


2 Resource submission basic: invalid url and resource rating
INPUT
- url: this_is_an_invalid_url
- resource usefulness rating: 2


3 Resource submission basic: not found url and resource rating
INPUT
- url: http://127.0.0.1:8000/notfoundurl
- resource usefulness rating: 3


4 Resource submission with tag and comments: url, resource rating, tag, comments
INPUT
- url: https://www.ualberta.ca/
- resource usefulness rating: 4
- tags: university, alberta, test (will need to add these tags to database before searching)
- comments: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa strong. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede link mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi.


5 Resource submission with tag, comments and attachment: url, resource rating, tag, comments, attachment
INPUT
- url: https://reactjs.org/
- resource usefulness rating: 5
- tags: react (will need to add these tags to database before searching)
- comments: React makes it painless to create interactive UIs. Design simple views for each state in your application, and React will efficiently update and render just the right components when your data changes.
- attachment: file

'''

# Generated by Selenium IDE
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
from ..models import Resource, Tag
sys.path.append('...')
from authentication.models import CustomUser

import time 


class TestResourceSubmission(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(50)
        super(TestResourceSubmission, self).setUp()

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestResourceSubmission, self).tearDown()

    def setup_test_db(self):

        CustomUser.objects.all().delete()
        Tag.objects.all().delete()
        Resource.objects.all().delete()

        self.user_email = "test@gmail.com"
        self.user_password = "test"
        user = CustomUser.objects.create_user(
            email=self.user_email,
            password=self.user_password
        )
        user.save()

        for tag_name in ["university", "alberta", "test", "react"]:
            tag = Tag.objects.create(name=tag_name)
            tag.save()

    def test_resource_submission(self):
        self.setup_test_db()

        self.driver.get("http://127.0.0.1:8000/chatbotportal/app")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.user_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()

        # Test url and rating
        actual_resource_detail = ["Google", "https://www.google.com/", "", ""]
        self.valid_resource_submission(actual_resource_detail, "//a/div/div")

        # Test invalid url and rating
        actual_resource_detail = ["", "this_is_an_invalid_url", "", ""]
        self.invalid_resource_submission(actual_resource_detail)

        # Test comment and tags (optional)
        actual_resource_detail = ["University of Alberta", "https://www.ualberta.ca/", "university,alberta,test", \
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa strong. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede link mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi."]
        self.valid_resource_submission(actual_resource_detail, "//a[2]/div/div", test_tags=True)

        # Test attachment (optional)
        actual_resource_detail = ["React – A JavaScript library for building user interfaces", "https://reactjs.org/", \
        "react", "React makes it painless to create interactive UIs. Design simple views for each state in your application, and React will efficiently update and render just the right components when your data changes."]
        self.valid_resource_submission(actual_resource_detail, "//a[3]/div/div", test_tags=True)


    def invalid_resource_submission(self, actual_resource_detail):
        self.submit_a_resource(actual_resource_detail)
        test_invalid_text = self.driver.find_element(By.XPATH, ("//form/div/div")).text
        assert "Please enter a url" == test_invalid_text

    def valid_resource_submission(self, actual_resource_detail, test_resource_path, test_tags=False):
        self.submit_a_resource(actual_resource_detail)
        test_valid_text = self.driver.find_element(By.XPATH, ("//p")).text
        time.sleep(1) # Sleep to wait for changes in db
        test_resource_detail = self.get_resource_detail(test_resource_path, test_tags=test_tags)

        assert "You've submitted a resource!" == test_valid_text 
        actual_resource_detail[2] = actual_resource_detail[2].replace(",","") # Get rid of commas for tags comparision
        # print (actual_resource_detail, test_resource_detail)
        assert actual_resource_detail == test_resource_detail

    def submit_a_resource(self, actual_resource_detail):
        [header, url, tags, comments] = actual_resource_detail

        self.driver.find_element(By.LINK_TEXT, "My Resources").click()
        self.driver.find_element(By.NAME, "submit_a_resource").click()
        self.driver.find_element(By.NAME, "url").send_keys(url)
        self.driver.find_element(By.NAME, "comments").send_keys(comments)
        for tag in tags.split(","):
            self.driver.find_element(By.XPATH, "//div[3]/div/div/input").send_keys(tag)
            self.driver.find_element(By.CSS_SELECTOR, ".ui > .search").send_keys(Keys.ENTER)
        # self.driver.find_element(By.XPATH, ("//i[2]")).click() # star rating
        time.sleep(1)
        self.driver.find_element(By.NAME, "submit").click()

    def get_resource_detail(self, resource_xpath, test_tags=False):
        self.driver.find_element(By.LINK_TEXT, "My Resources").click()
        self.driver.find_element(By.XPATH, (resource_xpath)).click()

        test_header = self.driver.find_element(By.XPATH, ("//h3")).text
        test_url = self.driver.find_element(By.CSS_SELECTOR, ".Resource__link____1ER80").text
        test_comments = self.driver.find_element(By.ID, "comments").text
        
        if test_tags:
            test_tags = self.driver.find_element(By.XPATH, ("//p[4]")).text
            test_tags = test_tags.replace("Tags:","")
            print("tags",test_tags)
        else:
            test_tags = ""

        # self.driver.find_element(By.CSS_SELECTOR, ".Resource__link____1ER80").click()
        return [test_header, test_url, test_tags, test_comments]