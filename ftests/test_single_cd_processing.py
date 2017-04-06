from os.path import expanduser
from time import sleep
from .base import FunctionalTest
from cdtool.settings import BASE_DIR

class AveragingSeriesTests(FunctionalTest):

    def test_can_submit_single_scan(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with one fieldset for input
        input_section = self.browser.find_element_by_id("input")
        file_upload = input_section.find_element_by_id("file-input")
        file_fieldsets = file_upload.find_elements_by_class_name("file-fieldset")
        self.assertEqual(len(file_fieldsets), 1)

        # The one file upload fieldset has a file input
        file_input = file_fieldsets[0].find_element_by_tag_name("input")
        self.assertEqual(file_input.get_attribute("type"), "file")

        # They submit a sample file with one scan in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/single-blank.dat")

        # They give the sample a name
        text_input = file_fieldsets[0].find_elements_by_tag_name("input")[1]
        self.assertEqual(text_input.get_attribute("type"), "text")
        text_input.send_keys("Test Sample I")

        # There is a config section, asking for the experiment name
        input_parameters = input_section.find_element_by_id("input-parameters")
        experiment_title_input = input_parameters.find_element_by_id("id_title")
        experiment_title_input.send_keys("A Single Sample Test")

        # They submit the data
        submit_button = input_section.find_elements_by_tag_name("input")[-1]
        submit_button.click()

        # They are still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The output section has a chart div
        output = self.browser.find_element_by_id("output")
        chart = output.find_element_by_id("chart")

        # The chart's title matches what was provided
        title = chart.find_element_by_class_name("highcharts-title")
        self.assertEqual(title.text, "A Single Sample Test")

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is only one line series
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 1)

        # The line series is just the scan from the file
        with open("ftests/test_data/single-blank.dat") as f:
            input_lines = f.readlines()
        lines = [l for l in lines if l.split()[0].split(".")[0].isdigit()]
        input_data = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in lines]
        chart_data = self.browser.execute_script(
         "return chart.series[1].data;"
        )
        self.assertEqual(chart_data, [l[:2] for l in input_data])

        # There is one area series
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # The area series is just the machine error from the chart
        chart_data = self.browser.execute_script(
         "return chart.series[1].data;"
        )
        for wavelength, error_min, error_max in chart_data:
            input_wavelength = [l for l in input_data if l[0] == wavelength][0]
            self.assertAlmostEqual(
             error_max - error_min, input_wavelength[2], delta=0.005
            )

        # Below the chart is the config section
        config = output.find_element_by_id("chart-config")

        # There config div has a div for the series
        series_div = config.find_element_by_id("series-config")
        series_div_title = series_div.find_element_by_class_name("series-title")
        self.assertEqual(series_div_title.text, "Test Sample I")

        # There is an option for displaying error
        error_option = series_div.find_element_by_id("error_option")
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # There is an option for displaying the series at all
        display_option = series_div.find_element_by_id("display_option")
        display_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 0)
        display_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 1)

        # The error can be hidden while the series is not visible
        display_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 0)
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 0)
        display_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 1)
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # Below the config div is the file output div
        file_output = output.find_element_by_id("file-output")

        # There is a button to download a data file
        download_button = file_output.find_element_by_id("file-download")

        # Clicking it produces a file with the correct name and data
        download_button.click()
        with open(expanduser("~") + "/Downloads/A Single Sample Test.dat") as f:
            output_lines = f.readlines()
        wavelengths = [l[0] for l in input_lines]
        output_lines = [l for l in output_lines if l.startswith(str(wavelength))]
        output_lines = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in output_lines]
        self.assertEqual(input_lines, output_lines)


    def test_can_submit_multiple_scans_in_one_file(self):
        pass


    def test_can_submit_multiple_scans_in_multiple_files(self):
        pass



class SubtractingSeriesTests(FunctionalTest):

    def test_can_subtract_single_scan_from_multiple_scans(self):
        pass


    def test_can_subtract_multiple_scans_from_multiple_scans(self):
        pass


    def test_can_subtract_multiple_files_from_multiple_files(self):
        pass




class SingleCdErrorTests(FunctionalTest):

    def test_error_when_no_file_given(self):
        pass


    def test_error_when_no_file_given_for_second_file_input(self):
        pass


    def test_error_when_no_series_found(self):
        pass


    def test_error_when_no_series_found_for_second_file_input(self):
        pass
