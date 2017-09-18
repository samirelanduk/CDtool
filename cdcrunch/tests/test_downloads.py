from datetime import datetime
from time import tzname
import json
from unittest.mock import patch, Mock
from cdtool.tests import ViewTest
from cdtool import version
from cdcrunch.downloads import *

class FilenameProductionTests(ViewTest):

    def test_can_peoduce_default_filename(self):
        self.assertEqual(produce_filename(""), "cdresults.dat")


    def test_can_append_dat(self):
        self.assertEqual(produce_filename("string"), "string.dat")


    def test_can_replace_spaces(self):
        self.assertEqual(produce_filename("str ing"), "str_ing.dat")


    def test_can_go_to_lower_case(self):
        self.assertEqual(produce_filename("String"), "string.dat")


    def test_invalid_characters_replaced(self):
        self.assertEqual(produce_filename("s:trin@g"), "s-trin-g.dat")



class SeriesToFileTests(ViewTest):

    def test_can_produce_file_with_current_version(self):
        filetext = series_to_file(json.dumps({"series": [], "error": []}))
        self.assertIn(version, filetext)


    def test_can_produce_file_with_current_date(self):
        filetext = series_to_file(json.dumps({"series": [], "error": []}))
        self.assertIn(datetime.now().strftime("%Y"), filetext)
        self.assertIn(datetime.now().strftime("%B"), filetext)
        self.assertIn(datetime.now().strftime("%A"), filetext)


    def test_can_produce_file_with_current_time(self):
        filetext = series_to_file(json.dumps({"series": [], "error": []}))
        self.assertIn(datetime.now().strftime("%H"), filetext)
        self.assertIn(datetime.now().strftime("%M"), filetext)
        self.assertIn(tzname[0], filetext)


    def test_can_produce_file_with_series_data(self):
        filetext = series_to_file(json.dumps({
         "series": [[190.0, 2.158], [191.0, 1.372], [192.0, 1.171]],
         "error": [[190.0, 1.7, 2.6], [191.0, 1.0, 1.7], [192.0, 0.9, 1.4]]
        }))
        lines = filetext.split("\n")[-3:]
        lines = [line.split() for line in lines]
        self.assertEqual(lines[0], ["192.0", "1.1710", "0.2500"])
        self.assertEqual(lines[1], ["191.0", "1.3720", "0.3500"])
        self.assertEqual(lines[2], ["190.0", "2.1580", "0.4500"])
