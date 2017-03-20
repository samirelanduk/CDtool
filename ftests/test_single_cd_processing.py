from .base import FunctionalTest
from time import sleep
from cdtool.settings import BASE_DIR

class AveragingSeriesTests(FunctionalTest):

    def test_can_submit_single_blank_file(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The blank entry section has a file input and a submit button
        file_input = blank_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        blank_submit = blank_input.find_elements_by_tag_name("input")[-1]
        self.assertEqual(blank_submit.get_attribute("type"), "submit")

        # They submit a blank file with a single scan in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/single-blank.dat")
        blank_submit.click()

        # They are still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The output section has a chart div
        output = self.browser.find_element_by_id("output")
        chart = output.find_element_by_id("chart")

        # The chart has a title with the word 'blank' in it
        title = chart.find_element_by_class_name("highcharts-title")
        self.assertIn("blank", title.text.lower())

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is a single line series
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        self.assertEqual(len(lines), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        download_button.click()

        # There is a downloaded file in Downloads
        with open("~/Downloads/TEST_DOWNLOAD") as f:
            lines = f.read()

        # The data in this file has two columns, and goes from 280 to 190
        data = [line.split() for line in lines]
        for line in data:
            self.assertEqual(len(line), 2)
        self.assertEqual(
         [float(line[0]) for line in data],
         list(range(190, 281))[::-1]
        )


    def test_can_submit_multi_scan_single_blank_file(self):
        pass


    def test_can_submit_multiple_blank_files(self):
        pass


    def test_graceful_errors_on_blank_submission_tests(self):
        pass


    def test_can_submit_single_sample_file(self):
        pass


    def test_can_submit_multi_scan_single_sample_file(self):
        pass


    def test_can_submit_multiple_sample_files(self):
        pass


    def test_graceful_errors_on_sample_submission_tests(self):
        pass