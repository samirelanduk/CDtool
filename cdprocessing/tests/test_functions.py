from django.test import TestCase
from cdprocessing.functions import clean_file, get_float_groups
from cdprocessing.functions import float_groups_to_series, extract_wavelengths
from cdprocessing.functions import extract_absorbances

class FileCleaningTests(TestCase):

    def test_can_clean_file_lines(self):
        cleaned = clean_file([
         b"$SUMMARY\n",
         b"Experiment Type : Wavelength\n",
         b"Experiment Name : Test Single Blank\n",
         b"\n",
         b"258.000 0.081 0.105 1.013 0.001 252.7 19.99\n"
        ])
        self.assertEqual(cleaned, [
         "$SUMMARY",
         "Experiment Type : Wavelength",
         "Experiment Name : Test Single Blank",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99"
        ])



class FloatGrouperTests(TestCase):

    def test_can_create_float_groups(self):
        float_groups = get_float_groups([
         "Irrelevant string1",
         "Irrelevant string2",
         "3 76 34",
         "4.5 4 32",
         "76.8 34 3",
         "More random data",
         "67.4 45",
         "45.6 4 4 4",
         "String 3",
         "7.4 7.4",
         "String 4"
        ])
        self.assertEqual(float_groups, [
         ["3 76 34", "4.5 4 32", "76.8 34 3"],
         ["67.4 45", "45.6 4 4 4"],
         ["7.4 7.4"]
        ])



class FloatGroupsToSeriesTests(TestCase):

    def test_can_get_single_series_from_float_groups(self):
        series = float_groups_to_series([
         ["3 76 34", "4.5 4 32", "76.8 34 3"],
         ["67.4 45", "45.6 4 4 4"],
         ["7.4 7.4"]
        ])
        self.assertEqual(series, ["3 76 34", "4.5 4 32", "76.8 34 3"])



class WavelengthsExtractionTests(TestCase):

    def test_can_pull_out_wavelengths_from_series(self):
        wavelengths = extract_wavelengths(["3 76 34", "4.5 4 32", "76.8 34 3"])
        self.assertEqual(wavelengths, [3.0, 4.5, 76.8])



class AbsorbanceExtractionTests(TestCase):

    def test_can_get_absorbance_from_series(self):
        absorbance = extract_absorbances(["3 76 34", "4.5 4 32", "76.8 34 3"])
        self.assertEqual(absorbance, [[3, 76], [4.5, 4], [76.8, 34]])
