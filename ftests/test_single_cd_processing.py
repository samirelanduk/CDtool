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

        # The main config div has a title and two buttons
        title = main_config.find_element_by_class_name("config-title")
        self.assertEqual(title.text, "Test Sample I")
        buttons = main_config.find_elements_by_tag_name("button")
        self.assertEqual(len(buttons), 2)
        toggle_series_button, toggle_error_button = buttons

        # Tne two buttons are both 'on'
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))

        # The error button can make the error disappear and reappear
        toggle_error_button.click()
        self.check_visible_area_series_count(chart_div, 0)
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.check_visible_area_series_count(chart_div, 1)
        self.assertIn("on", toggle_error_button.get_attribute("class"))

        # The series button can make everything disappear and reappear
        toggle_series_button.click()
        self.check_visible_area_series_count(chart_div, 0)
        self.check_visible_line_series_count(chart_div, 0)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        toggle_series_button.click()
        self.check_visible_area_series_count(chart_div, 1)
        self.check_visible_line_series_count(chart_div, 1)
        self.assertIn("on", toggle_series_button.get_attribute("class"))

        # The error can be hidden while the series is not visible
        toggle_series_button.click()
        self.check_visible_area_series_count(chart_div, 0)
        self.check_visible_line_series_count(chart_div, 0)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.check_visible_area_series_count(chart_div, 0)
        self.check_visible_line_series_count(chart_div, 0)
        self.assertIn("off", toggle_series_button.get_attribute("class"))
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_series_button.click()
        self.check_visible_area_series_count(chart_div, 0)
        self.check_visible_line_series_count(chart_div, 1)
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("off", toggle_error_button.get_attribute("class"))
        toggle_error_button.click()
        self.check_visible_area_series_count(chart_div, 1)
        self.check_visible_line_series_count(chart_div, 1)
        self.assertIn("on", toggle_series_button.get_attribute("class"))
        self.assertIn("on", toggle_error_button.get_attribute("class"))

        # The download section has a button to download the data - they click
        download_button = download_div.find_element_by_id("file-download")
        download_button.click()

        # They are still on the same page and the chart is still there
        self.check_page("/single/")
        self.check_chart_appears(chart_div)

        # This downloads a file with the correct data
        self.check_file_has_data("a_single_sample_test.dat", input_data)


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
        self.check_file_has_data("a_single_gen_sample_test.dat", input_data)



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
        sleep(1)
        self.check_chart_appears(chart_div)

        # The chart has the correct title
        self.check_chart_title(chart_div, "Multiple Sample Test")

        # The chart x axis goes from 190 to 280
        self.check_chart_x_axis(190, 280)








'''class AveragingSeriesTests(FunctionalTest):

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
