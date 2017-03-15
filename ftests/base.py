import os
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.current_location = os.path.dirname(os.path.realpath(__file__))
        self.browser.set_window_size(700, 600)


    def tearDown(self):
        self.browser.quit()
