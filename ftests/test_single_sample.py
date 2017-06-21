from datetime import datetime
from time import sleep
from cdtool.settings import BASE_DIR
from .base import FunctionalTest

class SingleScanTests(FunctionalTest):

    def test_can_crunch_single_scan(self):
        # The user goes to the main page
        self.get("/")

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
        file_input, name_input = scansinput.find_elements_by_tag_name("input")[:2]

        # A single scan is provided
        file_input.send_keys(BASE_DIR + "/ftests/test_data/single-sample.dat")
        name_input.send_keys("A very simple sample")

        # There is a configuration div
        configdiv = inputdiv.find_element_by_id("input-config")

        # The user enters the experiment name
        exp_name_input = configdiv.find_elements_by_tag_name("input")[0]
        exp_name_input.send_keys("Test Experiment")

        # The user submits the data
        submit_button = inputdiv.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # The user is still on the same page
        self.check_page("/")

         # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("chart-config")
        download_div = output_div.find_element_by_id("download")

        # The chart section has a chart in it
        sleep(1)
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "Test Experiment")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)

        # There is a single line series
        self.check_visible_line_series_count(chart_div, 1)

        # The line series matches the scan in the input data
        self.check_line_matches_data("sample", [w[:2] for w in input_data])

        # There is a single error series
        self.check_visible_area_series_count(chart_div, 1)

        # The error series matches the scan error in the input data
        self.check_error_matches_data(
         "sample_error",
         [[w[0], w[1] - w[2], w[1] + w[2]] for w in input_data]
        )




    def test_can_crunch_single_gen_scan(self):
        pass


    def test_error_on_no_file_sent(self):
        pass


    def test_error_if_no_scans_found(self):
        pass



class MultipleScanTests(FunctionalTest):

    def test_can_crunch_multiple_scans(self):
        pass


    def test_can_crunch_multiple_files(self):
        pass



class SingleScanSingleBlankTests(FunctionalTest):

    def test_can_crunch_one_scan_with_one_blank(self):
        pass


    def test_can_crunch_scan_and_blank_gens(self):
        pass


    def test_error_on_no_blank_file_given(self):
        pass


    def test_error_on_no_blank_scans_found(self):
        pass



class MultipleScanSingleBlankTests(FunctionalTest):

    def test_can_crunch_multiple_scans_with_one_blank(self):
        pass



class SingleScanMultipleBlankTests(FunctionalTest):

    def test_can_crunch_single_scan_with_multiple_blanks(self):
        pass


    def test_can_crunch_single_scan_with_multiple_blank_files(self):
        pass



class MultipleScanMultipleBlankTests(FunctionalTest):

    def test_can_submit_multiple_scans_with_multiple_blanks(self):
        pass
