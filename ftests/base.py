import os
from os.path import expanduser
from math import sqrt
from time import sleep
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


    def get(self, url):
        self.browser.get(self.live_server_url + url)


    def check_page(self, url):
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + url
        )


    def get_single_scan_from_file(self, file_name):
        with open("ftests/test_data/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        input_data = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in lines][::-1]
        return input_data


    def get_single_gen_scan_from_file(self, file_name):
        with open("ftests/test_data/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        input_data = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[5])
        ) for l in lines][::-1]
        return input_data


    def get_multiple_scans_from_file(self, file_name):
        with open("ftests/test_data/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        wavelengths = sorted(list(set([float(l.split()[0]) for l in lines])))
        input_data = []
        for wav in wavelengths:
            relevant_lines = [l for l in lines if float(l.split()[0]) == wav]
            values = [float(l.split()[1]) for l in relevant_lines]
            mean = sum(values) / len(values)
            sd = sqrt(sum([(val - mean) ** 2 for val in values]) / len(values))
            input_data.append([
             wav, mean, sd, values
            ])
        return input_data


    def combine_data_files(self, *data_files):
        wavelengths = [line[0] for line in data_files[0]]
        input_data = []
        for wav in wavelengths:
            relevant_lines = [[l for l in f if l[0] == wav][0] for f in data_files]
            values = [l[1] for l in relevant_lines]
            mean = sum(values) / len(values)
            sd = sqrt(sum([(val - mean) ** 2 for val in values]) / len(values))
            input_data.append([
             wav, mean, sd, values
            ])
        return input_data


    def subtract_data_files(self, sample, blank):
        wavelengths = [line[0] for line in sample]
        input_data = []
        for wav in wavelengths:
            sample_line, blank_line = [
             [l for l in f if l[0] == wav][0] for f in (sample, blank)
            ]
            sub = sample_line[1] - blank_line[1]
            error = sample_line[2] + blank_line[2]
            input_data.append([
             wav, sub, error, sample_line, blank_line
            ])
        return input_data


    def supply_input_data(self, input_div, input_sample_files="", input_blank_files="", sample_name="", blank_name="", experiment_name=""):
        # The input section has a file input section, a parameter section, and a
        # submit button
        file_input_div = input_div.find_element_by_id("file-input")
        input_parameter_div = input_div.find_element_by_id("input-parameters")
        submit_button = input_div.find_element_by_id("submit-input")

        # The file input section has a section for samples and a section for
        # blanks
        sample_input_div = file_input_div.find_element_by_id("sample-input")
        blank_input_div = file_input_div.find_element_by_id("blank-input")

        # The blank input section is pretty much empty
        self.assertEqual(
         len(blank_input_div.find_elements_by_tag_name("input")), 0
        )

        # The sample input section has inputs for files and sample name
        sample_file_input = sample_input_div.find_elements_by_tag_name("input")[0]
        sample_name_input = sample_input_div.find_elements_by_tag_name("input")[1]
        self.assertEqual(sample_file_input.get_attribute("type"), "file")
        self.assertEqual(sample_name_input.get_attribute("type"), "text")

        # They submit a sample file and name it
        sample_file_input.send_keys(input_sample_files)
        sample_name_input.send_keys(sample_name)

        # Blank files?
        if input_blank_files:
            # The blank input section has a clickable button
            blank_button = blank_input_div.find_element_by_tag_name("button")

            # They click it and make a new input div materialise
            blank_button.click()
            blank_file_input = blank_input_div.find_elements_by_tag_name("input")[0]
            blank_name_input = blank_input_div.find_elements_by_tag_name("input")[1]
            self.assertEqual(blank_file_input.get_attribute("type"), "file")
            self.assertEqual(blank_name_input.get_attribute("type"), "text")

            # They change their mind and want to make it disappear
            close_button = blank_input_div.find_element_by_tag_name("button")
            close_button.click()

            # Things are back to how they were before
            self.assertEqual(
             len(blank_input_div.find_elements_by_tag_name("input")), 0
            )
            blank_button = blank_input_div.find_element_by_tag_name("button")

            # They change their mind again and open the blank input again
            blank_button.click()
            blank_file_input = blank_input_div.find_elements_by_tag_name("input")[0]
            blank_name_input = blank_input_div.find_elements_by_tag_name("input")[1]
            self.assertEqual(blank_file_input.get_attribute("type"), "file")
            self.assertEqual(blank_name_input.get_attribute("type"), "text")

            # They submit a baseline file and name it
            blank_file_input.send_keys(input_blank_files)
            blank_name_input.send_keys(blank_name)

        # The parameters section asks for the experiment name
        experiment_name_div = input_parameter_div.find_element_by_id("experiment-name")
        experiment_name_input = experiment_name_div.find_element_by_tag_name("input")

        # They give it a name
        experiment_name_input.send_keys(experiment_name)

        # They submit the data
        submit_button.click()

        # They are still on the same page
        self.check_page("/single/")


    def check_chart_appears(self, chart_div):
        sleep(1)
        self.assertGreater(chart_div.size["width"], 10)
        self.assertGreater(chart_div.size["height"], 10)
        y_offset = self.browser.execute_script('return window.pageYOffset;')
        self.assertGreater(y_offset, 100)


    def check_chart_title(self, chart_div, title):
        title_element = chart_div.find_element_by_class_name("highcharts-title")
        self.assertEqual(title_element.text, title)
        title_text = self.browser.execute_script("return chart.title.textStr;")
        self.assertEqual(title_text, title)


    def check_chart_x_axis(self, x_min, x_max):
        self.assertEqual(
         self.browser.execute_script("return chart.xAxis[0].min;"), x_min
        )
        self.assertEqual(
         self.browser.execute_script("return chart.xAxis[0].max;"), x_max
        )


    def count_visible_lines(self, chart_div):
        lines = chart_div.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        return len(lines)


    def count_visible_areas(self, chart_div):
        areas = chart_div.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        return len(areas)


    def check_visible_line_series_count(self, chart_div, count):
        self.assertEqual(self.count_visible_lines(chart_div), count)


    def check_visible_area_series_count(self, chart_div, count):
        self.assertEqual(self.count_visible_areas(chart_div), count)


    def check_line_matches_data(self, line, data):
        line_length = self.browser.execute_script(
         "return chart.get('%s').data.length" % line
        )
        self.assertEqual(line_length, len(data))
        for index, datum in enumerate(data):
            self.assertEqual(
             datum[0],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].x;" % (line, index)
             )
            )
            self.assertAlmostEqual(
             datum[1],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].y;" % (line, index)
             ), delta=0.0005
            )


    def check_error_matches_data(self, error, data):
        error_length = self.browser.execute_script(
         "return chart.get('%s').data.length" % error
        )
        self.assertEqual(error_length, len(data))
        for index, datum in enumerate(data):
            self.assertEqual(
             datum[0],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].x;" % (error, index)
             )
            )
            self.assertAlmostEqual(
             datum[1],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].low;" % (error, index)
             ), delta=0.0005
            )
            self.assertAlmostEqual(
             datum[2],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].high;" % (error, index)
             ), delta=0.0005
            )


    def check_config_div_controls_series(self, chart_div, config, series_name, error_name, title_text):
        lines_at_start = self.count_visible_lines(chart_div)
        areas_at_start = self.count_visible_areas(chart_div)

        # The config div has a title and two buttons
        title = config.find_element_by_class_name("config-title")
        self.assertEqual(title.text, title_text)
        buttons = config.find_elements_by_tag_name("button")
        self.assertEqual(len(buttons), 2)
        toggle_series_button, toggle_error_button = buttons

        # Tne two buttons are both 'on'
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))

        # The error button can make the error disappear and reappear
        toggle_error_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.assertIn("on", toggle_error_button.get_attribute("class"))

        # The series button can make everything disappear and reappear
        toggle_series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        toggle_series_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", toggle_series_button.get_attribute("class"))

        # The error can be hidden while the series is not visible
        toggle_series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))


    def check_file_has_data(self, filename, data):
        with open(expanduser("~") + "/Downloads/{}".format(filename)) as f:
            output_lines = f.readlines()
        output_lines = [l for l in output_lines if l[:3].isdigit()]
        output_data = [tuple([float(c) for c in l.split()]) for l in output_lines]
        self.assertEqual(len(output_lines), len(data))
        for index, line in enumerate(output_data):
            for vindex, value in enumerate(line):
                self.assertAlmostEqual(value, data[index][vindex], delta=0.005)
