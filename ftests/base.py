import os
from os.path import expanduser
from math import sqrt
from time import sleep
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from cdtool.settings import BASE_DIR

class FunctionalTest(StaticLiveServerTestCase):

    # Setup and Teardown code
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


    # General checks
    def get(self, url):
        self.browser.get(self.live_server_url + url)


    def check_page(self, url):
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + url
        )


    # File readers
    def get_aviv_data(self, file_name):
        """Gets file data in the form [
         [wav, cd, error, [scans]]
        ]"""

        with open("ftests/files/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        input_data = [[
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ] for l in lines]
        return input_data


    def get_old_gen_data(self, file_name):
        with open("ftests/files/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        input_data = [[
         float(l.split()[0]), float(l.split()[1]), float(l.split()[5])
        ] for l in lines]
        return input_data


    def average(self, data):
        wavelengths = []
        for line in data:
            if line[0] not in wavelengths:
                wavelengths.append(line[0])
        averaged_data = []
        for wav in wavelengths:
            lines = [line for line in data if line[0] == wav]
            mean = sum([l[1] for l in lines]) / len(lines)
            sd = sqrt(sum([(val - mean) ** 2 for _, val, error in lines]) / len(lines))
            line = [wav, mean, sd, *lines]
            averaged_data.append(line)
        return averaged_data



    '''def get_single_gen_scan_from_file(self, file_name):
        with open("ftests/test_data/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        input_data =[(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[5])
        ) for l in lines]
        return input_data


    def get_multiple_scans_from_file(self, file_name):
        with open("ftests/test_data/" + file_name) as f:
            lines = f.readlines()
        lines = [l for l in lines if l[:3].isdigit()]
        wavelengths = sorted(list(set([float(l.split()[0]) for l in lines])))[::-1]
        input_data = []
        for wav in wavelengths:
            relevant_lines = [l for l in lines if float(l.split()[0]) == wav]
            values = [
             (float(l.split()[1]), float(l.split()[2])) for l in relevant_lines
            ]
            mean = sum([v[0] for v in values]) / len(values)
            sd = sqrt(sum([(val - mean) ** 2 for val, error in values]) / len(values))
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
    '''

    # Input checks
    def input_data(self, files="", sample_name="", exp_name=""):
        # There is an input section but no output section
        inputdiv = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        # There is a single sample input div
        sampleinputs = inputdiv.find_elements_by_class_name("sample-input")
        self.assertEqual(len(sampleinputs), 1)
        sampleinput = sampleinputs[0]

        # The sample input has a div for uploading scans
        scansinputs = sampleinput.find_elements_by_class_name("scans-input")
        self.assertEqual(len(scansinputs), 1)
        scansinput = scansinputs[0]

        # The scans input has inputs for files and sample name
        fileinput, nameinput = scansinput.find_elements_by_tag_name("input")[:2]

        # The sample scans are uploaded
        if files:
            fileinput.send_keys("{}/ftests/files/{}".format(BASE_DIR, files))
        nameinput.send_keys(sample_name)

        # There is a configuration div
        configdiv = inputdiv.find_element_by_id("input-config")

        # The user enters the experiment name
        exp_name_input = configdiv.find_elements_by_tag_name("input")[0]
        exp_name_input.send_keys(exp_name)

        # The user submits the data
        submit_button = inputdiv.find_elements_by_tag_name("input")[-1]
        submit_button.click()


    def check_error_message(self, message):
        # There is no output section
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        # There is an error message
        inputdiv = self.browser.find_element_by_id("input")
        error = inputdiv.find_element_by_class_name("error-message")
        self.assertIn(message, error.text)


    # Output checks
    def check_output_section_there(self):
        output_div = self.browser.find_element_by_id("output")
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("chart-config")
        download_div = output_div.find_element_by_id("download")


    def check_chart_ok(self, title, xmin, xmax, input_data):
        # Chart is correct size
        output_div = self.browser.find_element_by_id("output")
        chart_div = output_div.find_element_by_id("chart")
        sleep(1)
        self.assertGreater(chart_div.size["width"], 10)
        self.assertGreater(chart_div.size["height"], 10)
        y_offset = self.browser.execute_script('return window.pageYOffset;')
        self.assertGreater(y_offset, 100)

        # Title is ok
        title_element = chart_div.find_element_by_class_name("highcharts-title")
        self.assertEqual(title_element.text, title)
        title_text = self.browser.execute_script("return chart.title.textStr;")
        self.assertEqual(title_text, title)

        # x axis is correct
        self.assertEqual(
         self.browser.execute_script("return chart.xAxis[0].min;"), xmin
        )
        self.assertEqual(
         self.browser.execute_script("return chart.xAxis[0].max;"), xmax
        )

        # There is one line and one area
        self.assertEqual(self.count_visible_areas(chart_div), 1)
        self.assertEqual(self.count_visible_lines(chart_div), 1)

        # Series are correct
        self.check_line_matches_data("sample", input_data)
        self.check_area_matches_data("sample_error", input_data)
        # If there are component scans, they're fine too
        if len(input_data[0]) > 3:
            for scan_number in range(len(input_data[0]) - 3):
                scan = [row[scan_number + 3] for row in input_data]
                self.check_line_matches_data(
                 "sample_scan_{}".format(scan_number), scan
                )
                self.check_area_matches_data(
                 "sample_scan_{}_error".format(scan_number), scan
                )


    def check_chart_config_ok(self, sample_name, data):
        # The config div has one sample div
        output_div = self.browser.find_element_by_id("output")
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("chart-config")
        sample_divs = config_div.find_elements_by_class_name("sample-config")
        self.assertEqual(len(sample_divs), 1)
        sample_div = sample_divs[0]
        self.browser.execute_script("arguments[0].scrollIntoView();", sample_div)

        # The sample div has a main config div
        main_config = sample_div.find_element_by_class_name("main-config")

        # The main config contains the sample name
        sample_name_div = main_config.find_element_by_class_name("sample-name")
        self.assertEqual(sample_name_div.text, sample_name)

        # The main config also has a series controller
        main_series_controller = main_config.find_element_by_class_name("series-control")
        self.check_controller_controls_series(main_series_controller, "sample", data)

        # If there is only one one scan, that is it
        if len(data[0]) == 3:
            divs = main_config.find_elements_by_xpath("./*")
            self.assertEqual(len(divs), 2)
            divs = sample_div.find_elements_by_xpath("./*")
            self.assertEqual(len(divs), 1)
        else:
            # There are input scans
            show_more = main_config.find_element_by_class_name("show-more")
            show_all = main_config.find_element_by_class_name("show-all")
            scan_count = len(data[0]) - 3

            # Clicking the show-all button shows all
            lines_at_start = self.count_visible_lines(chart_div)
            areas_at_start = self.count_visible_areas(chart_div)
            show_all.click()
            self.check_visible_area_series_count(chart_div, areas_at_start + scan_count)
            self.check_visible_line_series_count(chart_div, lines_at_start + scan_count)
            show_all.click()
            self.check_visible_area_series_count(chart_div, areas_at_start)
            self.check_visible_line_series_count(chart_div, lines_at_start)
            show_all.click()
            self.check_visible_area_series_count(chart_div, areas_at_start + scan_count)
            self.check_visible_line_series_count(chart_div, lines_at_start + scan_count)

            # There is a hidden scans section
            scans_section = sample_div.find_element_by_class_name("scans-config")
            self.assertEqual(
             scans_section.value_of_css_property("display"),
             "none"
            )

            # Clicking show-more makes it visible
            show_more.click()
            sleep(0.75)
            self.assertEqual(
             scans_section.value_of_css_property("display"),
             "block"
            )

            # There are the right number of scan rows
            scan_configs = scans_section.find_elements_by_class_name("scan-config")
            self.assertEqual(len(scan_configs), 3)

            # They all work
            for index, config in enumerate(scan_configs):
                controller = config.find_element_by_class_name("series-control")
                self.check_controller_controls_series(controller, "sample_scan_{}".format(index), data)

            # Clicking show-more again hides it again
            show_more.click()
            sleep(0.75)
            self.assertEqual(
             scans_section.value_of_css_property("display"),
             "none"
            )


    def check_controller_controls_series(self, controller, series_name, data):
        output_div = self.browser.find_element_by_id("output")
        chart_div = output_div.find_element_by_id("chart")
        lines_at_start = self.count_visible_lines(chart_div)
        areas_at_start = self.count_visible_areas(chart_div)
        error_name = series_name + "_error"

        # Controller has two buttons
        buttons = controller.find_elements_by_tag_name("button")
        self.assertEqual(len(buttons), 2)
        series_button, error_button = buttons

        # Tne two buttons are both 'on'
        self.assertIn("on", series_button.get_attribute("class"))
        self.assertIn("on", error_button.get_attribute("class"))

        # The error button can make the error disappear and reappear
        error_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.assertIn("off", error_button.get_attribute("class"))
        error_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.assertIn("on", error_button.get_attribute("class"))

        # The series button can make everything disappear and reappear
        series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", series_button.get_attribute("class"))
        series_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", series_button.get_attribute("class"))

        # The error can be hidden while the series is not visible
        series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", series_button.get_attribute("class"))
        self.assertIn("on", error_button.get_attribute("class"))
        error_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start - 1)
        self.assertIn("off", series_button.get_attribute("class"))
        self.assertIn("off", error_button.get_attribute("class"))
        series_button.click()
        self.assertFalse(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start - 1)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", series_button.get_attribute("class"))
        self.assertIn("off", error_button.get_attribute("class"))
        error_button.click()
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % error_name
        ))
        self.assertTrue(self.browser.execute_script(
         "return chart.get('%s').visible" % series_name
        ))
        self.check_visible_area_series_count(chart_div, areas_at_start)
        self.check_visible_line_series_count(chart_div, lines_at_start)
        self.assertIn("on", series_button.get_attribute("class"))
        self.assertIn("on", error_button.get_attribute("class"))


    def check_file_download_ok(self, filename, file_data):
        # The download div has a button for downloading a datafile
        output_div = self.browser.find_element_by_id("output")
        download_div = output_div.find_element_by_id("download")
        download_button = download_div.find_element_by_id("download-button")
        self.browser.execute_script("arguments[0].scrollIntoView();", download_button)

        # Clicking does not make the user leave the page
        download_button.click()
        self.check_page("/")
        self.assertTrue(download_div.is_displayed())

        # This downloads a file with the correct data
        with open(expanduser("~") + "/Downloads/{}".format(filename)) as f:
            output_lines = f.readlines()
        output_lines = [l for l in output_lines if l[:3].isdigit()]
        output_data = [tuple([float(c) for c in l.split()]) for l in output_lines]
        self.assertEqual(len(output_lines), len(file_data))
        for index, line in enumerate(output_data):
            for vindex, value in enumerate(line):
                self.assertAlmostEqual(value, file_data[index][vindex], delta=0.005)


    def count_visible_lines(self, chart_div):
        lines = chart_div.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        return len(lines)


    def count_visible_areas(self, chart_div):
        areas = chart_div.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        return len(areas)


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


    def check_area_matches_data(self, error, data):
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
             datum[1] - datum[2],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].low;" % (error, index)
             ), delta=0.0005
            )
            self.assertAlmostEqual(
             datum[1] + datum[2],
             self.browser.execute_script(
              "return chart.get('%s').data[%i].high;" % (error, index)
             ), delta=0.0005
            )


    def check_visible_line_series_count(self, chart_div, count):
        self.assertEqual(self.count_visible_lines(chart_div), count)


    def check_visible_area_series_count(self, chart_div, count):
        self.assertEqual(self.count_visible_areas(chart_div), count)
