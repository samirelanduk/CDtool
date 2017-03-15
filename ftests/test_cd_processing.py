from .base import FunctionalTest
from time import sleep

class SingleRunAnalysisTests(FunctionalTest):

    def test_blank_alone_analysis(self):
        # The user goes to the single scan page
        self.browser.get(self.live_server_url + "/single/")

        # There is a section for inputting files
        file_section = self.browser.find_element_by_id("file-input")

        # There is an output section but it has no chart in it
        output_section = self.browser.find_element_by_id("output")
        chart = output_section.find_element_by_id("chart")
        self.assertEqual(chart.value_of_css_property("height"), "0px")

        # This has a div for blank entry and a div for sample entry
        blank_entry = file_section.find_element_by_id("blank-entry")
        sample_entry = file_section.find_element_by_id("sample-entry")

        # The blank entry has a file input
        form = blank_entry.find_element_by_tag_name("form")
        file_input = form.find_element_by_tag_name("input")
        self.assertEqual(file_input.get_attribute("type"), "file")

        # The user uploads a data file with one blank scan in it
        file_input.send_keys(
         self.current_location + "/test_data/single-blank.dat"
        )
        submit_button = form.find_elements_by_tag_name("input")[-1]
        self.assertEqual(submit_button.get_attribute("type"), "submit")
        submit_button.click()

        # They are still on the single entry page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # There is an output section that now takes up space
        output_section = self.browser.find_element_by_id("output")
        chart = output_section.find_element_by_id("chart")
        self.assertGreater(chart.value_of_css_property("height"), "0px")

        # The x axis goes from 190 to 280
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is a line series
        line = chart.find_element_by_class_name("highcharts-graph")
