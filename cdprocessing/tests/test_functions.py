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



'''class SeriesExtractionTests(TestCase):

    def test_can_pull_out_series_from_file_lines(self):
        series = extract_series([
         "$SUMMARY",
         "Experiment Type : Wavelength",
         "Experiment Name : Test Single Blank",
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99",
         "$CONFIGURATION",
         "$EXPNAME:Flowthrow Apols A835 #1",
         "$NDATAPOINTS:91",
         "$VERSION:v3.44",
         "$EXTYPE:1",
         "$EXNAME:Flowthrow Apols A835"
        ])
        self.assertEqual(series, [
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])


    def test_can_pull_out_series_when_there_is_irrelevant_numeric_data_present(self):
        series = extract_series([
         "$SUMMARY",
         "Experiment Type : Wavelength",
         "Experiment Name : Test Single Blank",
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99",
         "$CONFIGURATION",
         "$EXPNAME:Flowthrow Apols A835 #1",
         "$NDATAPOINTS:91",
         "$VERSION:v3.44",
         "1.0 2.0 3.0",
         "4.4 6.5 8.8",
         "$EXTYPE:1",
         "$EXNAME:Flowthrow Apols A835"
        ])
        self.assertEqual(series, [
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])


    def test_can_handle_missing_headers(self):
        series = extract_series([
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99",
         "$CONFIGURATION",
         "$EXPNAME:Flowthrow Apols A835 #1",
         "$NDATAPOINTS:91",
         "$VERSION:v3.44",
         "$EXTYPE:1",
         "$EXNAME:Flowthrow Apols A835"
        ])
        self.assertEqual(series, [
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])


    def test_headers_omitted_if_they_dont_look_right(self):
        series = extract_series([
         "$SUMMARY",
         "Experiment Type : Wavelength",
         "Experiment Name : Test Single Blank",
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99",
         "$CONFIGURATION",
         "$EXPNAME:Flowthrow Apols A835 #1",
         "$NDATAPOINTS:91",
         "$VERSION:v3.44",
         "$EXTYPE:1",
         "$EXNAME:Flowthrow Apols A835"
        ])
        self.assertEqual(series, [
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])



class WavelengthsExtractionTests(TestCase):

    def test_can_get_wavelengths_from_series(self):
        wavelengths = get_wavelengths([
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])
        self.assertEqual(
         wavelengths,
         [258.0, 257.0, 256.0, 255.0, 254.0, 253.0, 252.0, 251.0, 250.0]
        )


    def test_can_get_wavelengths_from_series_with_header(self):
        wavelengths = get_wavelengths([
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])
        self.assertEqual(
         wavelengths,
         [258.0, 257.0, 256.0, 255.0, 254.0, 253.0, 252.0, 251.0, 250.0]
        )



class AbsorbanceExtractionTests(TestCase):

    def test_can_get_absorbances_from_series(self):
        absorbances = get_absorbance([
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])
        self.assertEqual(
         absorbances,
         [
          [258.0, 0.081], [257.0, 0.267], [256.0, 0.190], [255.0, 0.034],
          [254.0, 0.245], [253.0, 0.036], [252.0, 0.086], [251.0, 0.017],
          [250.0, -0.038]
         ]
        )


    def test_can_get_absorbances_from_series_with_header(self):
        absorbances = get_absorbance([
         "X  CD_Signal  CD_Error  CD(Abs)  CD_Delta  CD_Dynode  Jacket_Temp.",
         "258.000 0.081 0.105 1.013 0.001 252.7 19.99",
         "257.000  0.267  0.219  1.013  0.003  253.6  19.98",
         "256.000  0.190  0.098  1.013  0.002  254.4  19.98",
         "255.000  0.034  0.084  1.013  0.000  255.1  19.99",
         "254.000  0.245  0.289  1.013  0.002  255.9  19.99",
         "253.000  0.036  0.060  1.013  0.000  256.6  19.98",
         "252.000  0.086  0.096  1.013  0.001  257.4  19.98",
         "251.000  0.017  0.129  1.013  0.000  258.1  19.99",
         "250.000  -0.038  0.129  1.013  -0.000  258.8  19.99"
        ])
        self.assertEqual(
         absorbances,
         [
          [258.0, 0.081], [257.0, 0.267], [256.0, 0.190], [255.0, 0.034],
          [254.0, 0.245], [253.0, 0.036], [252.0, 0.086], [251.0, 0.017],
          [250.0, -0.038]
         ]
        )'''
