from os.path import expanduser
from time import sleep
from .base import FunctionalTest
from cdtool.settings import BASE_DIR

class AveragingSeriesTests(FunctionalTest):

    def test_can_submit_single_blank_file(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The blank entry section has a file input and a submit button outside
        file_input = blank_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        blank_submit = input_section.find_elements_by_tag_name("input")[-1]
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
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        sleep(1)
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_blank.dat") as f:
            output_lines = f.readlines()

        # The data in this file is just the data from the original file
        wavelength_range = range(190, 281)
        with open("ftests/test_data/single-blank.dat") as f:
            input_lines = f.readlines()
        for wavelength in wavelength_range:
            input_value = [float(l.split()[1]) for l in input_lines
             if l.startswith(str(wavelength))][0]
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertEqual(input_value, output_value)


    def test_can_submit_multi_scan_single_blank_file(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The blank entry section has a file input and a submit button outside
        file_input = blank_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        blank_submit = input_section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(blank_submit.get_attribute("type"), "submit")

        # They submit a blank file with three scans in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/three-blanks.dat")
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
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is an error area around the line
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # Below the chart is a div for altering the chart appearance
        chart_config = output.find_element_by_id("chart-config")

        # They press the button for toggling input lines
        input_button = chart_config.find_element_by_id("toggle-inputs")
        sleep(1)
        input_button.click()

        # There are now four lines, but still only one area
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 4)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # They press the button again, and the three lines disappear
        input_button.click()
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_blank.dat") as f:
            output_lines = f.readlines()

        # The data in this file is the averaged data from the original file
        wavelength_range = range(190, 281)
        with open("ftests/test_data/three-blanks.dat") as f:
            input_lines = f.readlines()
        for wavelength in wavelength_range:
            input_values = [float(l.split()[1]) for l in input_lines
             if l.startswith(str(wavelength))]
            self.assertEqual(len(input_values), 3)
            average_input_value = sum(input_values) / len(input_values)
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertAlmostEqual(average_input_value, output_value, delta=0.005)

        # There is a third column containing the errors
        for wavelength in wavelength_range:
            line = [l for l in output_lines if l.startswith(str(wavelength))][0]
            self.assertEqual(len(line.split()), 3)
            self.assertGreater(float(line.split()[2]), 0.0)


    def test_can_submit_multiple_blank_files(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The blank entry section has a file input and a submit button outside
        file_input = blank_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        blank_submit = input_section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(blank_submit.get_attribute("type"), "submit")

        # They submit a blank file with three scans in it and one with one scan
        file_input.send_keys(
         "%s/ftests/test_data/three-blanks.dat\n%s/ftests/test_data/single-blank.dat" % (
          BASE_DIR, BASE_DIR
         )
        )
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
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is an error area around the line
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # Below the chart is a div for altering the chart appearance
        chart_config = output.find_element_by_id("chart-config")

        # They press the button for toggling input lines
        input_button = chart_config.find_element_by_id("toggle-inputs")
        sleep(1)
        input_button.click()

        # There are now five lines, but still only one area
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 5)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # They press the button again, and the four lines disappear
        input_button.click()
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_blank.dat") as f:
            output_lines = f.readlines()

        # The data in this file is the averaged data from the original files
        wavelength_range = range(190, 281)
        with open("ftests/test_data/three-blanks.dat") as f:
            input_lines_three = f.readlines()
        with open("ftests/test_data/single-blank.dat") as f:
            input_lines_one = f.readlines()
        for wavelength in wavelength_range:
            input_values = [float(l.split()[1]) for l in input_lines_three
             if l.startswith(str(wavelength))]
            input_values += [float(l.split()[1]) for l in input_lines_one
             if l.startswith(str(wavelength))]
            self.assertEqual(len(input_values), 4)
            average_input_value = sum(input_values) / len(input_values)
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertAlmostEqual(average_input_value, output_value, delta=0.005)

        # There is a third column containing the errors
        for wavelength in wavelength_range:
            line = [l for l in output_lines if l.startswith(str(wavelength))][0]
            self.assertEqual(len(line.split()), 3)
            self.assertGreater(float(line.split()[2]), 0.0)


    def test_graceful_errors_on_blank_submission_tests(self):
        pass


    def test_can_submit_single_sample_file(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The sample entry section has a file input and a submit button outside
        file_input = sample_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        sample_submit = input_section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(sample_submit.get_attribute("type"), "submit")

        # They submit a blank file with a single scan in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/single-sample.dat")
        sample_submit.click()

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
        self.assertIn("sample", title.text.lower())

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is a single line series
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        sleep(1)
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_sample.dat") as f:
            output_lines = f.readlines()

        # The data in this file is just the data from the original file
        wavelength_range = range(190, 281)
        with open("ftests/test_data/single-sample.dat") as f:
            input_lines = f.readlines()
        for wavelength in wavelength_range:
            input_value = [float(l.split()[1]) for l in input_lines
             if l.startswith(str(wavelength))][0]
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertEqual(input_value, output_value)


    def test_can_submit_multi_scan_single_sample_file(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The sample entry section has a file input and a submit button outside
        file_input = sample_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        sample_submit = input_section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(sample_submit.get_attribute("type"), "submit")

        # They submit a blank file with three scans in it
        file_input.send_keys(BASE_DIR + "/ftests/test_data/three-samples.dat")
        sample_submit.click()

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
        self.assertIn("sample", title.text.lower())

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is a single line series
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is an error area around the line
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # Below the chart is a div for altering the chart appearance
        chart_config = output.find_element_by_id("chart-config")

        # They press the button for toggling input lines
        input_button = chart_config.find_element_by_id("toggle-inputs")
        sleep(1)
        input_button.click()

        # There are now four lines, but still only one area
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 4)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # They press the button again, and the three lines disappear
        input_button.click()
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_sample.dat") as f:
            output_lines = f.readlines()

        # The data in this file is the averaged data from the original file
        wavelength_range = range(190, 281)
        with open("ftests/test_data/three-samples.dat") as f:
            input_lines = f.readlines()
        for wavelength in wavelength_range:
            input_values = [float(l.split()[1]) for l in input_lines
             if l.startswith(str(wavelength))]
            self.assertEqual(len(input_values), 3)
            average_input_value = sum(input_values) / len(input_values)
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertAlmostEqual(average_input_value, output_value, delta=0.005)

        # There is a third column containing the errors
        for wavelength in wavelength_range:
            line = [l for l in output_lines if l.startswith(str(wavelength))][0]
            self.assertEqual(len(line.split()), 3)
            self.assertGreater(float(line.split()[2]), 0.0)


    def test_can_submit_multiple_sample_files(self):
        # User goes to the single run page
        self.browser.get(self.live_server_url + "/single/")

        # There is a file input section, with two sub-sections
        input_section = self.browser.find_element_by_id("file-input")
        blank_input = input_section.find_element_by_id("blank-input")
        sample_input = input_section.find_element_by_id("sample-input")

        # The sample entry section has a file input and a submit button outside
        file_input = sample_input.find_elements_by_tag_name("input")[0]
        self.assertEqual(file_input.get_attribute("type"), "file")
        sample_submit = input_section.find_elements_by_tag_name("input")[-1]
        self.assertEqual(sample_submit.get_attribute("type"), "submit")

        # They submit a blank file with three scans in it and one with one scan
        file_input.send_keys(
         "%s/ftests/test_data/three-samples.dat\n%s/ftests/test_data/single-sample.dat" % (
          BASE_DIR, BASE_DIR
         )
        )
        sample_submit.click()

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
        self.assertIn("sample", title.text.lower())

        # The x-axis goes from 280 to 190
        x_axis = chart.find_element_by_class_name("highcharts-xaxis-labels")
        x_labels = x_axis.find_elements_by_tag_name("text")
        self.assertEqual(x_labels[0].text, "190")
        self.assertEqual(x_labels[-1].text, "280")

        # There is a single line series
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)

        # There is an error area around the line
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # Below the chart is a div for altering the chart appearance
        chart_config = output.find_element_by_id("chart-config")

        # They press the button for toggling input lines
        input_button = chart_config.find_element_by_id("toggle-inputs")
        sleep(1)
        input_button.click()

        # There are now five lines, but still only one area
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 5)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # They press the button again, and the four lines disappear
        input_button.click()
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)
        areas = chart.find_elements_by_class_name("highcharts-arearange-series")
        areas = [area for area in areas if area.is_displayed()]
        self.assertEqual(len(areas), 1)

        # There is a download button, which they click
        download_button = output.find_element_by_id("download")
        download_button.click()
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/single/"
        )

        # The chart and everything is still there
        chart = output.find_element_by_id("chart")
        title = chart.find_element_by_class_name("highcharts-title")
        lines = chart.find_elements_by_class_name("highcharts-line-series")
        lines = [line for line in lines if line.is_displayed()]
        self.assertEqual(len(lines), 1)


        # There is a downloaded file in Downloads
        with open(expanduser("~") + "/Downloads/average_sample.dat") as f:
            output_lines = f.readlines()

        # The data in this file is the averaged data from the original files
        wavelength_range = range(190, 281)
        with open("ftests/test_data/three-samples.dat") as f:
            input_lines_three = f.readlines()
        with open("ftests/test_data/single-sample.dat") as f:
            input_lines_one = f.readlines()
        for wavelength in wavelength_range:
            input_values = [float(l.split()[1]) for l in input_lines_three
             if l.startswith(str(wavelength))]
            input_values += [float(l.split()[1]) for l in input_lines_one
             if l.startswith(str(wavelength))]
            self.assertEqual(len(input_values), 4)
            average_input_value = sum(input_values) / len(input_values)
            output_value = [float(l.split()[1]) for l in output_lines
             if l.startswith(str(wavelength))][0]
            self.assertAlmostEqual(average_input_value, output_value, delta=0.005)

        # There is a third column containing the errors
        for wavelength in wavelength_range:
            line = [l for l in output_lines if l.startswith(str(wavelength))][0]
            self.assertEqual(len(line.split()), 3)
            self.assertGreater(float(line.split()[2]), 0.0)


    def test_graceful_errors_on_sample_submission_tests(self):
        pass
