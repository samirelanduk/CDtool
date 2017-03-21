import os
from os.path import expanduser
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.current_location = os.path.dirname(os.path.realpath(__file__))
        self.browser.set_window_size(800, 600)


    def tearDown(self):
        self.browser.quit()
        for name in ("average_blank", "average_sample"):
            try:
                os.remove(expanduser("~") + "/Downloads/%s.dat" % name)
            except OSError:
                pass
