
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

6 Resource submission not found url (should still saves to database)
= url: http://127.0.0.1:8000/


TEST OUTPUT
- click on resource and go to resource detail to compare if url, rating, tags, comments and attachement are the same as inputs
'''

# Generated by Selenium IDE
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
from ..models import Resource, Tag
sys.path.append('...')


class TestResourceSubmission(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(50)
        self.vars = {}
        self.setup_db()

        super(TestResourceSubmission, self).setUp()

    def setup_db(self):
        CustomUser.objects.all().delete()
        Tag.objects.all().delete()
        Resource.objects.all().delete()

        self.user_email = "test@gmail.com"
        self.user_password = "test"
        user = CustomUser.objects.create_user(
            email=self.user_email,
            password=self.user_password,
        )
        user.save()

        for tag_name in ["Alberta", "General_Health", "Public", "Research"]:
            tag = Tag.objects.create(name=tag_name)
            tag.save()

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        super(TestResourceSubmission, self).tearDown()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_resource_submission(self):
        
        self.driver.get('%s%s' % (self.live_server_url, "/chatbotportal/app"))
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.NAME, "email").send_keys(self.user_email)
        self.driver.find_element(
            By.NAME, "password").send_keys(self.user_password)
        self.driver.find_element(By.NAME, "login_button").click()

        # Test invalid url
        actual_resource_detail = ["", "this_is_an_invalid_url", "", "", "", "", ""]
        self.invalid_resource_submission(actual_resource_detail, "frontend")
        actual_resource_detail = ["", "www.google.com", "", "", "", "", ""]
        self.invalid_resource_submission(actual_resource_detail, "backend")

        # Test valid url
        actual_resource_detail = ["MyHealth.Alberta.ca", "https://myhealth.alberta.ca/", "Alberta",
                                  "A general resource regarding public health, provided by the Alberta government.",
                                  "pending", "Website", ""]
        self.valid_resource_submission(
            actual_resource_detail, "//a[1]/div/div")

        actual_resource_detail = ["Unknown title",
                                  "http://127.0.0.1:8000/", "", 
                                  "Even though this resource is not reachable, it is still accepted.",
                                  "pending", "Website", ""]
        self.valid_resource_submission(
            actual_resource_detail, "//a[2]/div/div")

        # Test valid url and PDF attachment
        actual_resource_detail = ["The Autism Research Institute | #1 Advocate for Autism Research | Home",
                                  "https://www.autism.org", "Research",
                                  "An institution dedicated to autism research.",
                                  "pending", "PDF",
                                  "ARI works to advance the understanding of autism by funding research and facilitating education on its causes and the potential treatments."
                                  ]
        self.valid_resource_submission(
            actual_resource_detail, "//a[3]/div/div")


    def invalid_resource_submission(self, actual_resource_detail,option):
        self.submit_a_resource(actual_resource_detail)
        if option == "frontend":
            # Invalid xpath
            test_invalid_text = self.driver.find_element(By.XPATH, ("//form/div/div/div")).text
            assert "Please enter a valid url" == test_invalid_text
        elif option == "backend":
            test_invalid_text = self.driver.find_element(By.NAME, ("submit_failure")).text
            assert "Something went wrong! Your resource is not submitted." == test_invalid_text

    def valid_resource_submission(self, actual_resource_detail, test_resource_path):
        self.submit_a_resource(actual_resource_detail)
        test_valid_text = self.driver.find_element(By.NAME, ("submit_success")).text
        time.sleep(2)  # Sleep to wait for changes in db
        test_resource_detail = self.get_resource_detail(test_resource_path)

        assert "Congratulations! You've submitted a resource!" == test_valid_text
        actual_resource_detail[2] = actual_resource_detail[2].replace(",", "")  # Get rid of commas for tags comparision
        print(actual_resource_detail, test_resource_detail)
        assert actual_resource_detail == test_resource_detail

    def submit_a_resource(self, actual_resource_detail):
        [header, url, tags, comments, review_status, category, website_summary] = actual_resource_detail

        self.driver.find_element(By.LINK_TEXT, "My Resources").click()

        self.driver.find_element(By.NAME, "submit_a_resource").click()
        self.driver.find_element(By.NAME, "url").send_keys(url)
        self.driver.find_element(By.NAME, "comments").send_keys(comments)

        # Category xpath
        if category == "PDF":
            self.driver.find_element(
                By.CSS_SELECTOR, ".fluid:nth-child(2)").click()
            self.driver.find_element(
                By.CSS_SELECTOR, ".visible > .item:nth-child(3)").click()
            self.attachment_path = str(os.path.join(
                os.path.dirname(__file__), "attachment_test.pdf"))
            self.driver.find_element(By.NAME, "attachment").send_keys(self.attachment_path)

        # Tags xpath
        for tag in tags.split(","):
            self.driver.find_element(
                By.XPATH, "//div[4]/div/div/input").send_keys(tag)
            self.driver.find_element(
                By.CSS_SELECTOR, ".ui > .search").send_keys(Keys.ENTER)

        self.driver.find_element(By.NAME, "submit").click()

    def get_resource_detail(self, resource_xpath):
        self.driver.find_element(By.LINK_TEXT, "My Resources").click()
        self.driver.find_element(By.XPATH, (resource_xpath)).click()

        test_header = self.driver.find_element(By.ID, "title_header").text.strip()
        test_url = self.driver.find_element(By.ID, "url").text
        test_comments = self.driver.find_element(By.ID, "comments").text
        test_review_status = self.driver.find_element(By.ID, "review_status").text
        test_category = self.driver.find_element(By.ID, "category").text
        test_website_summary = self.driver.find_element(By.ID, "website_summary_metadata").text
        
        # Download attachment
        if test_category == "PDF":
            self.download_and_compare_attachments()        

        # Tags xpath
        try:
            test_tags = self.driver.find_element(
                By.XPATH, ("//div[4]")).text
            test_tags = test_tags.replace("Tags:\n", "")
            # print("tags", test_tags)
        except:
            test_tags = ""

        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.ID, "url").click()
        self.vars["win7210"] = self.wait_for_window(2000)
        self.vars["root"] = self.driver.current_window_handle
        self.driver.switch_to.window(self.vars["win7210"])
        self.driver.close()
        self.driver.switch_to.window(self.vars["root"])

        return [test_header, test_url, test_tags, test_comments, test_review_status, test_category, test_website_summary]

    def download_and_compare_attachments(self):

        download_path = os.path.join(Path.home(), "Downloads")
        
        # Remove all attachment_test files
        for filename in os.listdir(download_path):
            if filename.startswith("attachment_test"):
                os.remove(os.path.join(download_path, filename))
        
        # Download and wait till finish
        self.driver.find_element(By.ID, "attachment").click()
        time.sleep(5)

        # Get just downloaded attachment_test
        for filename in os.listdir(download_path):
            if filename.startswith("attachment_test"):
                downloaded_pdf_text = textract.process(os.path.join(
                    download_path, filename), method='pdfminer')
        
        attachemnt_pdf_text = textract.process(self.attachment_path, method='pdfminer')
        assert attachemnt_pdf_text == downloaded_pdf_text
