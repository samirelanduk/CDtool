from datetime import datetime
from time import sleep
from .base import FunctionalTest

class SingleScanTests(FunctionalTest):

    def test_can_crunch_single_scan(self):
        pass


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
