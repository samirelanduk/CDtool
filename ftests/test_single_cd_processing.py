from math import sqrt
from time import sleep
import inferi
from .base import FunctionalTest
from cdtool.settings import BASE_DIR

class SingleSampleScanTests(FunctionalTest):

    def test_can_submit_single_scan(self):
        # Get data for this test
        input_data = self.get_single_scan_from_file("single-sample.dat")

        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section, but no output section
        input_div = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        self.supply_input_data(
         input_div,
         input_sample_files=BASE_DIR + "/ftests/test_data/single-sample.dat",
         sample_name="Test Sample I",
         experiment_name="A Single Sample Test"
        )

        # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("config")
        download_div = output_div.find_element_by_id("download")

        # The chart section has a chart in it
        sleep(1)
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "A Single Sample Test")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)

        # There is a single line series
        self.check_visible_line_series_count(chart_div, 1)

        # The line series matches the scan in the input data
        self.check_line_matches_data("main", [w[:2] for w in input_data])

        # There is a single error series
        self.check_visible_area_series_count(chart_div, 1)

        # The error series matches the scan error in the input data
        self.check_error_matches_data(
         "main_error",
         [[w[0], w[1] - w[2], w[1] + w[2]] for w in input_data]
        )

        # The config section has a single series config div for the main series
        main_config = config_div.find_element_by_id("main-config")
        self.assertEqual(len(config_div.find_elements_by_xpath("./*")), 1)
        self.assertIn("series-config", main_config.get_attribute("class"))

        # The config div controls the main series
        self.check_config_div_controls_series(
         chart_div, main_config, "main", "main_error", "Test Sample I"
        )

        # The download section has a button to download the data - they click
        download_button = download_div.find_element_by_id("file-download")
        download_button.click()

        # They are still on the same page and the chart is still there
        self.check_page("/single/")
        self.check_chart_appears(chart_div)

        # This downloads a file with the correct data
        self.check_file_has_data("a_single_sample_test.dat", input_data[::-1])


    def test_error_on_no_file_submission(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section
        input_div = self.browser.find_element_by_id("input")

        # They click the process data button
        submit_button = input_div.find_element_by_id("submit-input")
        submit_button.click()

        # They are still on the page
        self.check_page("/single/")

        # The input section now has an errors section
        input_div = self.browser.find_element_by_id("input")
        errors_div = input_div.find_element_by_id("errors")

        # The user is told they need to provide at least one file
        self.assertIn("at least one file", errors_div.text)


    def test_error_if_no_scans_found(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section and a file input
        input_div = self.browser.find_element_by_id("input")

        self.supply_input_data(
         input_div,
         input_sample_files=BASE_DIR + "/ftests/test_data/no-series.dat",
         sample_name="",
         experiment_name=""
        )

        # The input section now has an errors section
        input_div = self.browser.find_element_by_id("input")
        errors_div = input_div.find_element_by_id("errors")

        # The user is told they need to provide at least one scan
        self.assertIn("no scans", errors_div.text.lower())


    def test_can_submit_single_old_gen_scan(self):
        # Get data for this test
        input_data = self.get_single_gen_scan_from_file("single-gen-sample.gen")

        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section, but no output section
        input_div = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        # The user supplies input data
        self.supply_input_data(
         input_div,
         input_sample_files=BASE_DIR + "/ftests/test_data/single-gen-sample.gen",
         sample_name="Gen Sample",
         experiment_name="A Single Gen Sample Test"
        )

        # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("config")
        download_div = output_div.find_element_by_id("download")

        # The chart section has a chart in it
        sleep(1)
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "A Single Gen Sample Test")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)

        # There is a single line series
        self.check_visible_line_series_count(chart_div, 1)

        # The line series matches the scan in the input data
        self.check_line_matches_data("main", [w[:2] for w in input_data])

        # There is a single error series
        self.check_visible_area_series_count(chart_div, 1)

        # The error series matches the scan error in the input data
        self.check_error_matches_data(
         "main_error",
         [[w[0], w[1] - w[2], w[1] + w[2]] for w in input_data]
        )

        # The download section has a button to download the data - they click
        download_button = download_div.find_element_by_id("file-download")
        download_button.click()

        # They are still on the same page and the chart is still there
        self.check_page("/single/")
        self.check_chart_appears(chart_div)

        # This downloads a file with the correct data
        self.check_file_has_data("a_single_gen_sample_test.dat", input_data[::-1])



class MultipleSampleScanTests(FunctionalTest):

    def test_can_submit_multiple_scans(self):
        # Get data for this test
        input_data = self.get_multiple_scans_from_file("three-samples.dat")

        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section, but no output section
        input_div = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        # The user supplies input data
        self.supply_input_data(
         input_div,
         input_sample_files=BASE_DIR + "/ftests/test_data/three-samples.dat",
         sample_name="Multi Sample",
         experiment_name="Multiple Sample Test"
        )

        # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("config")
        download_div = output_div.find_element_by_id("download")

        # The chart section has a chart in it
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "Multiple Sample Test")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)

        # There is a single line series
        self.check_visible_line_series_count(chart_div, 1)

        # The line series matches the scan average in the input data
        self.check_line_matches_data("main", [w[:2] for w in input_data])

        # There is a single error series
        self.check_visible_area_series_count(chart_div, 1)

        # The error series matches the scan error in the input data
        self.check_error_matches_data(
         "main_error",
         [[w[0], w[1] - w[2], w[1] + w[2]] for w in input_data]
        )

        # The config section has a single series config div for the main series
        main_config = config_div.find_element_by_id("main-config")
        self.assertEqual(len(config_div.find_elements_by_xpath("./*")), 2)
        self.assertIn("series-config", main_config.get_attribute("class"))

        # The config div controls the main series
        self.check_config_div_controls_series(
         chart_div, main_config, "main", "main_error", "Multi Sample"
        )

        # The config section also has a sample scan section
        sample_scan_config = config_div.find_element_by_id("sample-scan-config")

        # It has a button for toggling sample scan visibility
        all_scan_toggle = sample_scan_config.find_element_by_tag_name("button")
        all_scan_toggle.click()
        self.check_visible_line_series_count(chart_div, 4)
        self.check_visible_area_series_count(chart_div, 4)
        for button in sample_scan_config.find_elements_by_tag_name("button"):
            self.assertNotIn(" off", button.get_attribute("class"))
        all_scan_toggle.click()
        self.check_visible_line_series_count(chart_div, 1)
        self.check_visible_area_series_count(chart_div, 1)
        for button in sample_scan_config.find_elements_by_tag_name("button"):
            self.assertNotIn(" on", button.get_attribute("class"))

        # The sample scan config section has three individual series config divs
        series_configs = sample_scan_config.find_elements_by_class_name("series-config")
        self.assertEqual(len(series_configs), 3)

        # Each one controls a series
        all_scan_toggle.click()
        for index, config in enumerate(series_configs, start=1):
            self.check_config_div_controls_series(
             chart_div, config, "sample_%i" % index, "sample_error_%i" % index, "Multi Sample #%i" % index
            )

        # The download section has a button to download the data - they click
        download_button = download_div.find_element_by_id("file-download")
        download_button.click()

        # They are still on the same page and the chart is still there
        self.check_page("/single/")
        self.check_chart_appears(chart_div)

        # This downloads a file with the correct data
        self.check_file_has_data("multiple_sample_test.dat", input_data[::-1])


    def test_can_submit_multiple_scans_in_multiple_files(self):
        # Get data for this test
        input_data1 = self.get_single_gen_scan_from_file("single-sample.dat")
        input_data2 = self.get_single_scan_from_file("single-gen-sample.gen")
        input_data = self.combine_data_files(input_data1, input_data2)

        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section, but no output section
        input_div = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

        # The user supplies input data
        self.supply_input_data(
         input_div,
         input_sample_files="{}/ftests/test_data/single-gen-sample.gen\n{}/ftests/test_data/single-sample.dat".format(BASE_DIR, BASE_DIR),
         sample_name="A Sample",
         experiment_name="Multi-File Sample Test"
        )

        # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("config")
        download_div = output_div.find_element_by_id("download")

        # The chart section has a chart in it
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "Multi-File Sample Test")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)

        # There is a single line series
        self.check_visible_line_series_count(chart_div, 1)

        # The line series matches the scan average in the input data
        self.check_line_matches_data("main", [w[:2] for w in input_data])

        # There is a single error series
        self.check_visible_area_series_count(chart_div, 1)

        # The error series matches the scan error in the input data
        self.check_error_matches_data(
         "main_error",
         [[w[0], w[1] - w[2], w[1] + w[2]] for w in input_data]
        )

        # The download section has a button to download the data - they click
        download_button = download_div.find_element_by_id("file-download")
        download_button.click()

        # They are still on the same page and the chart is still there
        self.check_page("/single/")
        self.check_chart_appears(chart_div)

        # This downloads a file with the correct data
        self.check_file_has_data("multi-file_sample_test.dat", input_data[::-1])
