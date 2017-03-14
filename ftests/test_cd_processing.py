from .base import FunctionalTest

class SingleRunAnalysisTests(FunctionalTest):

    def test_blank_alone_analysis(self):
        # The user goes to the single scan page
        self.browser.get(self.live_server_url + "/single/")

        # There is a section for inputting files
        file_section = self.browser.find_element_by_id("file-input")

        # This has a div for blank entry and a div for sample entry
        blank_entry = file_section.find_element_by_id("blank-entry")
        sample_entry = file_section.find_element_by_id("sample-entry")

        # The blank entry has a file input
        form = blank_entry.find_element_by_tag_name("form")
        file_input = form.find_element_by_tag_name("input")
        self.assertEqual(file_input.get_attribute("type"), "file")

        # The user uploads
