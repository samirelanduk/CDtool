from datetime import datetime
from time import sleep
from .base import FunctionalTest

class SingleScanTests(FunctionalTest):

    def test_can_crunch_single_aviv_scan(self):
        # Get expected data
        input_data = self.get_aviv_data("single-aviv.dat")

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan
        self.input_data(
         files="single-aviv.dat",
         sample_name="A very simple sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Test Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("A very simple sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("test_experiment.dat", input_data)


    def test_can_crunch_single_old_gen_scan(self):
        # Get expected data
        input_data = self.get_old_gen_data("single-old-gen.gen")

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan
        self.input_data(
         files="single-old-gen.gen",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Test Experiment", 190, 280, input_data[::-1])

        # The download section produces a file
        self.check_file_download_ok("test_experiment.dat", input_data)


    def test_error_on_no_file_sent(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("didn't submit any files")


    def test_error_on_no_scans_in_file(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="no-scans.dat",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no scans")


    def test_error_on_binary_file(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="binary.dat",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no scans")



class MultipleScanTests(FunctionalTest):

    def test_can_crunch_multiple_scans(self):
        # Get expected data
        input_data = self.get_aviv_data("three-aviv.dat")
        input_data = self.average(input_data)

        # The user goes to the main page
        self.get("/")

        # The user input smultiple AVIV scans
        self.input_data(
         files="three-aviv.dat",
         sample_name="A tri-scan sample",
         exp_name="Triple Scan Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Triple Scan Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("A tri-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("triple_scan_experiment.dat", input_data)


    def test_can_crunch_multiple_files(self):
        # Get expected data
        input_data1 = self.get_aviv_data("single-aviv.dat")
        input_data2 = self.get_old_gen_data("single-old-gen.gen")
        input_data = input_data1 + input_data2
        input_data = self.average(input_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan
        self.input_data(
         files=["single-aviv.dat", "single-old-gen.gen"],
         sample_name="A bi-scan sample",
         exp_name="Two File Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Two File Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("A bi-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("two_file_experiment.dat", input_data)




class SingleScanSingleBlankTests(FunctionalTest):

    def test_can_crunch_one_scan_with_one_blank(self):
        # Get expected data
        input_data = self.get_aviv_data("single-aviv.dat")
        baseline_data = self.get_aviv_data("single-aviv-baseline.dat")
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="single-aviv.dat",
         baseline_files="single-aviv-baseline.dat",
         sample_name="A bi-scan sample",
         exp_name="Two Scan Subtraction Experiment"
        )


    '''def test_can_crunch_scan_and_blank_gens(self):
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
        pass'''
