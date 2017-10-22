from datetime import datetime
from time import sleep
import shutil
import os
from os.path import expanduser
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

        # The user inputs a single .gen scan
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


    def test_can_crunch_pcddb_gen_scan(self):
        # Get expected data
        input_data = self.get_old_gen_data("single-pcddb-gen.gen")
        for line in input_data:
            line["error"] = 0

        # The user goes to the main page
        self.get("/")

        # The user inputs a single .gen scan
        self.input_data(
         files="single-pcddb-gen.gen",
         sample_name="PCDDB sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Test Experiment", 175, 300, input_data[::-1])

        # The download section produces a file
        self.check_file_download_ok("test_experiment.dat", input_data)


    def test_can_crunch_own_output_scan(self):
        # Get expected data
        input_data = self.get_old_gen_data("single-old-gen.gen")

        # The user goes to the main page
        self.get("/")

        # The user inputs a single old gen scan
        self.input_data(
         files="single-old-gen.gen",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The download section produces a file
        self.check_chart_ok("Test Experiment", 190, 280, input_data[::-1])
        self.check_file_download_ok("test_experiment.dat", input_data)

        # This is moved to files
        shutil.move(
         expanduser("~") + "/Downloads/test_experiment.dat",
         "ftests/files/test_experiment.dat"
        )
        try:
            # The user goes to the main page
            self.get("/")

            # The user inputs a single cdtool scan
            self.input_data(
             files="test_experiment.dat",
             sample_name="Gen sample",
             exp_name="Test Experiment 2"
            )

            # There is now an output section
            self.check_page("/")
            self.check_output_section_there()

            # The chart section has a chart in it
            self.check_chart_ok("Test Experiment 2", 190, 280, input_data[::-1])

            # The download section produces a file
            self.check_file_download_ok("test_experiment_2.dat", input_data)
        finally:
            os.remove("ftests/files/test_experiment.dat")



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

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Two Scan Subtraction Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("A bi-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("two_scan_subtraction_experiment.dat", input_data)


    def test_can_crunch_scan_and_blank_gens(self):
        # Get expected data
        input_data = self.get_old_gen_data("single-old-gen.gen")
        baseline_data = self.get_old_gen_data("single-old-gen-baseline.gen")
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="single-old-gen.gen",
         baseline_files="single-old-gen-baseline.gen",
         sample_name="A bi-scan sample",
         exp_name="Two Gen Subtraction Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Two Gen Subtraction Experiment", 190, 280, input_data[::-1])

        # The download section produces a file
        self.check_file_download_ok("two_gen_subtraction_experiment.dat", input_data)


    def test_error_on_no_raw_file_given(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="",
         baseline_files="single-old-gen-baseline.gen",
         sample_name="Gen sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no raw files")


    def test_error_on_no_raw_scans_found(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="no-scans.dat",
         baseline_files="single-aviv.dat",
         sample_name="sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no scans")
        self.check_error_message("raw")


    def test_error_on_no_blank_scans_found(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="single-aviv.dat",
         baseline_files="no-scans.dat",
         sample_name="sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no scans")
        self.check_error_message("baseline")


    def test_error_on_no_neither_scans_found(self):
        # The user goes to the main page
        self.get("/")

        # The user inputs no files
        self.input_data(
         files="no-scans.dat",
         baseline_files="no-scans.dat",
         sample_name="sample",
         exp_name="Test Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is an error message
        self.check_error_message("no scans")



class MultipleScanSingleBlankTests(FunctionalTest):

    def test_can_crunch_multiple_scans_with_one_blank(self):
        # Get expected data
        input_data = self.get_aviv_data("three-aviv.dat")
        input_data = self.average(input_data)
        baseline_data = self.get_old_gen_data("single-old-gen-baseline.gen")
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="three-aviv.dat",
         baseline_files="single-old-gen-baseline.gen",
         sample_name="Penta-scan sample",
         exp_name="Averaging Subtraction Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Averaging Subtraction Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("Penta-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("averaging_subtraction_experiment.dat", input_data)



class SingleScanMultipleBlankTests(FunctionalTest):

    def test_can_crunch_single_scan_with_multiple_blanks(self):
        # Get expected data
        input_data = self.get_aviv_data("single-aviv.dat")
        baseline_data = self.get_aviv_data("three-aviv-baseline.dat")
        baseline_data = self.average(baseline_data)
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="single-aviv.dat",
         baseline_files="three-aviv-baseline.dat",
         sample_name="Penta-scan sample",
         exp_name="Averaging Subtraction Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Averaging Subtraction Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("Penta-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("averaging_subtraction_experiment.dat", input_data)


    def test_can_crunch_single_scan_with_multiple_blank_files(self):
        # Get expected data
        input_data = self.get_aviv_data("single-aviv.dat")
        baseline_data1 = self.get_aviv_data("single-aviv-baseline.dat")
        baseline_data2 = self.get_old_gen_data("single-old-gen-baseline.gen")
        baseline_data = baseline_data1 + baseline_data2
        baseline_data = self.average(baseline_data)
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="single-aviv.dat",
         baseline_files=["single-aviv-baseline.dat", "single-old-gen-baseline.gen"],
         sample_name="Penta-scan sample",
         exp_name="Averaging Subtraction Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Averaging Subtraction Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("Penta-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("averaging_subtraction_experiment.dat", input_data)



class MultipleScanMultipleBlankTests(FunctionalTest):

    def test_can_submit_multiple_scans_with_multiple_blanks(self):
        # Get expected data
        input_data = self.get_aviv_data("three-aviv.dat")
        input_data = self.average(input_data)
        baseline_data = self.get_aviv_data("three-aviv-baseline.dat")
        baseline_data = self.average(baseline_data)
        input_data = self.subtract(input_data, baseline_data)

        # The user goes to the main page
        self.get("/")

        # The user inputs a single AVIV scan and a single AVIV baseline scan
        self.input_data(
         files="three-aviv.dat",
         baseline_files="three-aviv-baseline.dat",
         sample_name="Hexa-scan sample",
         exp_name="Averaging Subtraction Experiment"
        )

        # The user is still on the same page
        self.check_page("/")

        # There is now an output section
        self.check_output_section_there()

        # The chart section has a chart in it
        self.check_chart_ok("Averaging Subtraction Experiment", 190, 280, input_data[::-1])

        # The config section controls the chart
        self.check_chart_config_ok("Hexa-scan sample", input_data)

        # The download section produces a file
        self.check_file_download_ok("averaging_subtraction_experiment.dat", input_data)
