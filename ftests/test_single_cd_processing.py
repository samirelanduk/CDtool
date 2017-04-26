from os.path import expanduser
from math import sqrt
from time import sleep
import inferi
from .base import FunctionalTest
from cdtool.settings import BASE_DIR

class SingleSampleScanTests(FunctionalTest):

    def test_can_submit_single_scan(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is an input section, but no output section
        input_div = self.browser.find_element_by_id("input")
        self.assertEqual(len(self.browser.find_elements_by_id("output")), 0)

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

        # They submit a sample file with one scan in it
        sample_file_input.send_keys(
         BASE_DIR + "/ftests/test_data/single-sample.dat"
        )
        sample_name_input.send_keys("Test Sample I")

        # The parameters section asks for the experiment name
        experiment_name_div = input_parameter_div.find_element_by_id("experiment-name")
        experiment_name_input = experiment_name_div.find_element_by_tag_name("input")

        # They give it a name
        experiment_name_input.send_keys("A Single Sample Test")

        # They submit the data
        submit_button.click()

        # They are still on the same page
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # There is now an output section
        output_div = self.browser.find_element_by_id("output")

        # It has sections for the chart, for configuration, and downloading
        chart_div = output_div.find_element_by_id("chart")
        config_div = output_div.find_element_by_id("config")
        download_div = output_div.find_element_by_id("download")

        '''# The output section has a chart div
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
        with open("ftests/test_data/single-sample.dat") as f:
            input_lines = f.readlines()
        lines = [l for l in input_lines if l[:3].isdigit()]
        input_data = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in lines]
        for index, line in enumerate(input_data):
            self.assertEqual(
             line[0],
             self.browser.execute_script("return chart.get('main').data[%i].x;" % index)
            )
            self.assertEqual(
             line[1],
             self.browser.execute_script("return chart.get('main').data[%i].y;" % index)
            )

        # There is one area series
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # The area series is just the machine error from the chart
        for index, line in enumerate(input_data):
            self.assertEqual(
             line[0],
             self.browser.execute_script("return chart.get('main_error').data[%i].x;" % index)
            )
            error_low = self.browser.execute_script("return chart.get('main_error').data[%i].low;" % index)
            error_high = self.browser.execute_script("return chart.get('main_error').data[%i].high;" % index)
            self.assertAlmostEqual(2 * line[2], error_high - error_low, delta=0.005)


        # Below the chart is the config section
        config = output.find_element_by_id("chart-config")

        # The config div has a div for the main series
        main_series_div = config.find_element_by_id("main-series-config")
        main_div_title = main_series_div.find_element_by_class_name("series-title")
        self.assertEqual(main_div_title.text, "Test Sample I")

        # There is an option for displaying error
        error_option = main_series_div.find_element_by_class_name("error-option")
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # There is an option for displaying the series at all
        display_option = main_series_div.find_element_by_class_name("display-option")
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
        output_lines = [l for l in output_lines if l[:3].isdigit()]
        output_lines = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in output_lines]
        self.assertEqual(input_data, output_lines)



class AveragingSeriesTests(FunctionalTest):

    def test_can_submit_multiple_scans_in_one_file(self):
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

        # They submit a sample file with three scans in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/three-samples.dat")

        # They give the sample a name
        text_input = file_fieldsets[0].find_elements_by_tag_name("input")[1]
        self.assertEqual(text_input.get_attribute("type"), "text")
        text_input.send_keys("Test Sample II")

        # There is a config section, asking for the experiment name
        input_parameters = input_section.find_element_by_id("input-parameters")
        experiment_title_input = input_parameters.find_element_by_id("id_title")
        experiment_title_input.send_keys("A Multiple Sample Test")

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
        self.assertEqual(title.text, "A Multiple Sample Test")

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is only one line series
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 1)

        # The line series is the average of the scans from the file
        with open("ftests/test_data/three-samples.dat") as f:
            input_lines = f.readlines()
        lines = [l for l in input_lines if l[:3].isdigit()]
        input_data = [(
         float(l.split()[0]), float(l.split()[1]), float(l.split()[2])
        ) for l in lines]
        wavelengths = sorted(list(set([l[0] for l in input_data])))
        input_data = [{
         "wavelength": wavelength,
         "input_values": inferi.Series(*[l[1] for l in input_data if l[0] == wavelength], sample=False)
        } for wavelength in wavelengths]
        for index, line in enumerate(input_data[::-1]):
            self.assertEqual(
             line["wavelength"],
             self.browser.execute_script("return chart.get('main').data[%i].x;" % index)
            )
            self.assertEqual(
             line["input_values"].mean(),
             self.browser.execute_script("return chart.get('main').data[%i].y;" % index)
            )

        # There is one area series
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # The area series is the standard error of the three series
        for index, line in enumerate(input_data[::-1]):
            self.assertEqual(
             line["wavelength"],
             self.browser.execute_script("return chart.series[0].data[%i].x;" % index)
            )
            self.assertEqual(
             line["input_values"].mean() - line["input_values"].standard_deviation(),
             self.browser.execute_script("return chart.series[0].data[%i].low;" % index)
            )
            self.assertEqual(
             line["input_values"].mean() + line["input_values"].standard_deviation(),
             self.browser.execute_script("return chart.series[0].data[%i].high;" % index)
            )

        # Below the chart is the config section
        config = output.find_element_by_id("chart-config")

        # The config div has a div for the main series
        main_series_div = config.find_element_by_id("main-series-config")
        main_div_title = main_series_div.find_element_by_class_name("series-title")
        self.assertEqual(main_div_title.text, "Test Sample II")

        # There is an option for displaying error
        error_option = main_series_div.find_element_by_class_name("error-option")
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        error_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 1)

        # There is an option for displaying the series at all
        display_option = main_series_div.find_element_by_class_name("display-option")
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

        # The user turns off the main series
        display_option.click()
        area_series = self.get_visible_area_series(chart)
        self.assertEqual(len(area_series), 0)
        line_series = self.get_visible_line_series(chart)
        self.assertEqual(len(line_series), 0)

        # There is a div for sample scans
        sample_scans = config.find_element_by_id("sample-scans")

        # It has three series div
        sample_series_divs = sample_scans.find_elements_by_class_name("series-config")
        self.assertEqual(len(sample_series_divs), 3)

        # Each div controls a line
        for index, sample_series_div in enumerate(sample_series_divs):
            sample_div_title = sample_series_div.find_element_by_class_name("series-title")
            self.assertEqual(sample_div_title.text, "Test Sample II #%i" % (index + 1))


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
        pass'''
