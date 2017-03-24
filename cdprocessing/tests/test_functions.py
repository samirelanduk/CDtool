from django.test import TestCase
from cdprocessing.functions import clean_file, get_float_groups
from cdprocessing.functions import float_groups_to_big_series
from cdprocessing.functions import float_groups_to_extra_series
from cdprocessing.functions import extract_wavelengths
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



class FloatGroupsToBiggestSeriesTests(TestCase):

    def test_can_get_single_series_from_float_groups(self):
        series = float_groups_to_big_series([
         ["67.4 45", "45.6 4 4 4"],
         ["3 76 34", "4.5 4 32", "76.8 34 3"],
         ["7.4 7.4"]
        ])
        self.assertEqual(series, ["3 76 34", "4.5 4 32", "76.8 34 3"])



class FloatGroupsToMultipleSeriesTests(TestCase):

    def test_can_get_additional_series_from_float_groups_and_big_series(self):
        extra_series = float_groups_to_extra_series([
         ["67.4 45", "45.6 4 4 4"],
         ["3 76 34", "4.5 4 32", "76.8 34 3"],
         ["7.4 7.4"],
         ["3 34 2", "4.5 45 17", "76.8 3 7"],
         ["3 1 42", "4.5 45 87", "76.8 321 1"],
        ], ["3 76 34", "4.5 4 32", "76.8 34 3"])
        self.assertEqual(
         extra_series,
         [["3 34 2", "4.5 45 17", "76.8 3 7"], ["3 1 42", "4.5 45 87", "76.8 321 1"]]
        )



class WavelengthsExtractionTests(TestCase):

    def test_can_pull_out_wavelengths_from_series(self):
        wavelengths = extract_wavelengths(["3 76 34", "4.5 4 32", "76.8 34 3"])
        self.assertEqual(wavelengths, [3.0, 4.5, 76.8])



class AbsorbanceExtractionTests(TestCase):

    def test_can_get_absorbance_from_single_series(self):
        absorbance = extract_absorbances([["3 76 34", "4.5 4 32", "76.8 34 3"]])
        self.assertEqual(absorbance, [[3, 76], [4.5, 4], [76.8, 34]])


    def test_can_get_absorbance_from_multiple_series(self):
        absorbance = extract_absorbances([
         ["3 76 34", "4.5 4 32", "76.8 34 3"],
         ["3 71 34", "4.5 1 32", "76.8 19.8 3"],
         ["3 78 34", "4.5 4 32", "76.8 96.2 3"]
        ])
        self.assertEqual(absorbance, [[3, 75], [4.5, 3], [76.8, 50]])
