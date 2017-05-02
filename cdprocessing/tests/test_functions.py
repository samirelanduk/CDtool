from unittest.mock import patch, Mock
from cdtool.tests import ViewTest
from cdprocessing.functions import *

class AllSeriesExtractionFromFileTests(ViewTest):

    @patch("cdprocessing.functions.get_float_groups")
    @patch("cdprocessing.functions.remove_short_float_groups")
    @patch("cdprocessing.functions.remove_incorrect_wavelengths")
    @patch("cdprocessing.functions.remove_short_lines")
    @patch("cdprocessing.functions.strip_float_groups")
    def test_extractor_calls_correct_functions(self, *mocks):
        float_groups = Mock()
        len_filtered_float_groups = Mock()
        wav_filtered_float_groups = Mock()
        line_filtered_float_groups = Mock()
        stripped_float_groups = Mock()
        mock_strip, mock_line_filter, mock_wav_filter, mock_len_filter, mock_get = mocks
        mock_get.return_value = float_groups
        mock_len_filter.return_value = len_filtered_float_groups
        mock_wav_filter.return_value = wav_filtered_float_groups
        mock_line_filter.return_value = line_filtered_float_groups
        mock_strip.return_value = stripped_float_groups
        series = extract_all_series(self.test_file)
        stripped_lines = [
         "$MDCDATA:1:14:2:3:4:9",
         "100 200 300",
         "X  CD_Signal  CD_Error  CD_Current_(Abs)",
         "279.000  1.0  0.5  1.013  -0.000  242.9  19.98",
         "278.000  -4.0  0.4  1.013  0.000  243.2  19.99",
         "277.000  12.0  0.3  1.013  0.000  243.5  19.99"
        ]
        mock_get.assert_called_with(stripped_lines)
        mock_len_filter.assert_called_with(float_groups)
        mock_wav_filter.assert_called_with(len_filtered_float_groups)
        mock_line_filter.assert_called_with(wav_filtered_float_groups)
        mock_strip.assert_called_with(line_filtered_float_groups)
        self.assertIs(series, stripped_float_groups)



class FloatGrouperTests(ViewTest):

    def test_can_find_float_groups(self):
        float_groups = get_float_groups([
         "Irrelevant string1",
         "Irrelevant string2",
         "3 76 34",
         "4.5 4 32",
         "76.8 34 3",
         "More random data",
         "67.4 45",
         "45.6 4 4 4",
         "67.6 string",
         "7.4 7.4",
         "String 4"
        ])
        self.assertEqual(float_groups, [
         [[3, 76, 34], [4.5, 4, 32], [76.8, 34, 3]],
         [[67.4, 45], [45.6, 4, 4, 4]],
         [[7.4, 7.4]]
        ])


    def test_float_groups_returns_nothing_if_no_float_groups(self):
        float_groups = get_float_groups([
         "Irrelevant string1",
         "Irrelevant string2",
         "More random data",
         "67.6 string",
         "String 4"
        ])
        self.assertEqual(float_groups, [])



class ShortFloatGroupRemovalTests(ViewTest):

    def test_can_filter_zero_float_groups(self):
        self.assertEqual(remove_short_float_groups([]), [])


    def test_can_remove_short_groups(self):
        filtered_groups = remove_short_float_groups([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[67.4, 45, 1], [45.6, 4, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[7.4, 7.4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]]
        ])



class IncorrectWavelengthRemovalTests(ViewTest):

    def test_can_filter_zero_float_groups(self):
        self.assertEqual(remove_incorrect_wavelengths([]), [])


    def test_can_remove_incorrect_wavelengths(self):
        filtered_groups = remove_incorrect_wavelengths([
         [[3, 76, 1], [4.5, 4, 1], [75.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])



class ShortLineRemovalTests(ViewTest):

    def test_can_filter_zero_float_groups(self):
        self.assertEqual(remove_short_lines([]), [])


    def test_can_remove_short_lines(self):
        filtered_groups = remove_short_lines([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76], [4.5, 4], [76.8, 34]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])



class FloatGroupStrippingTests(ViewTest):

    def test_can_strip_zero_float_groups(self):
        self.assertEqual(strip_float_groups([]), [])


    def test_stripping_len_3_lines_does_nothing(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_just_uses_3_values_per_line(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 1, 10], [4.5, 4, 1, 11], [76.8, 34, 1, 10]],
         [[3, 76, 1, 9], [4.5, 4, 1, 3], [76.8, 34, 1, 8]],
         [[3, 74, 1, 2], [4.5, 5, 1, 4], [76.8, 4, 1, 5]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_negative_columns(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, -1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, -1, 1]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_100_columns(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, 101, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, 101, 1]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_columns_that_are_entirely_zero(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 0, 0, 1], [4.5, 4, 0, 0, 1], [76.8, 34, 0, 0, 1]],
         [[3, 76, 0, 0, 1], [4.5, 4, 0, 0, 1], [76.8, 34, 0, 0, 1]],
         [[3, 74, 0, 0, 1], [4.5, 5, 0, 0, 1], [76.8, 4, 0, 0, 1]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_handles_running_out_of_columns(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, 101, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, 101, -1]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])


    def test_stripping_handles_all_zeroes_columns(self):
        stripped_groups = strip_float_groups([
         [[3, 76, 0, 0, 0], [4.5, 4, 0, 0, 0], [76.8, 34, 0, 0, 0]],
         [[3, 76, 0, 0, 0], [4.5, 4, 0, 0, 0], [76.8, 34, 0, 0, 0]],
         [[3, 74, 0, 0, 0], [4.5, 5, 0, 0, 0], [76.8, 4, 0, 0, 0]]
        ])
        self.assertEqual(stripped_groups, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])



class SeriesAveragingTests(ViewTest):

    def test_can_average_one_series(self):
        average = average_series([[
         [279, 1, 0.5], [278, 2, 0.4], [277, 3, 0.2]
        ]])
        self.assertEqual(average, [
         [279, 1, 0.5], [278, 2, 0.4], [277, 3, 0.2]
        ])


    def test_can_average_multple_series(self):
        average = average_series([
         [[279, -0.006, 0], [278, 0.042, 0], [277, 0.036, 0]],
         [[279, -0.047, 0], [278, 0.04, 0], [277, -0.275, 0]],
         [[279, -0.34, 0], [278, 0.01, 0], [277, -0.18, 0]]
        ])
        self.assertEqual(len(average), 3)
        self.assertEqual(average[0][0], 279)
        self.assertEqual(average[1][0], 278)
        self.assertEqual(average[2][0], 277)
        self.assertAlmostEqual(average[0][1], -0.131, delta=0.005)
        self.assertAlmostEqual(average[1][1], 0.0307, delta=0.005)
        self.assertAlmostEqual(average[2][1], -0.1397, delta=0.005)
        self.assertAlmostEqual(average[0][2], 0.1487, delta=0.005)
        self.assertAlmostEqual(average[1][2], 0.01464, delta=0.005)
        self.assertAlmostEqual(average[2][2], 0.1301, delta=0.005)



class FileNamerTests(ViewTest):

    def test_can_replace_spaces_with_underscores(self):
        self.assertEqual(get_file_name("a file name"), "a_file_name")


    def test_can_force_lower_case(self):
        self.assertEqual(get_file_name("FILENAME"), "filename")
