import os
from os.path import expanduser
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.current_location = os.path.dirname(os.path.realpath(__file__))
        self.files_at_start = os.listdir(expanduser("~") + "/Downloads")


    def tearDown(self):
        self.browser.quit()
        files_at_end = os.listdir(expanduser("~") + "/Downloads")
        to_remove = [
         f for f in files_at_end if f not in self.files_at_start and f[-4:] == ".dat"
        ]
        for f in to_remove:
            os.remove(expanduser("~") + "/Downloads/%s" % f)


    def check_chart_appears(self, chart_div):
        self.assertGreater(chart_div.size["width"], 10)
        self.assertGreater(chart_div.size["height"], 10)
        y_offset = self.browser.execute_script('return window.pageYOffset;')
        self.assertGreater(y_offset, 100)


    def get_visible_line_series(self, div):
        lines = div.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        return lines


    def get_visible_area_series(self, div):
        areas = div.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        return areas
