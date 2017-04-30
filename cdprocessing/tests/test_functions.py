from unittest.mock import patch
from cdtool.tests import ViewTest
from cdprocessing.functions import extract_all_series, get_float_groups
from cdprocessing.functions import filter_float_groups, average_series
from cdprocessing.functions import get_file_name

class AllSeriesExtractionFromFileTests(ViewTest):

    @patch("cdprocessing.functions.get_float_groups")
    def test_extractor_passes_file_lines_to_float_extractor(self, test_get):
        test_get.return_value = [[[100, 200, 300]], [[279, 2, 3]]]
        series = extract_all_series(self.single_scan_file)
        stripped_lines = [
         "$MDCDATA:1:14:2:3:4:9",
         "100 200 300",
         "X  CD_Signal  CD_Error  CD_Current_(Abs)",
         "279.000  1.0  0.5  1.013  -0.000  242.9  19.98",
         "278.000  -4.0  0.4  1.013  0.000  243.2  19.99",
         "277.000  12.0  0.3  1.013  0.000  243.5  19.99"
        ]
        test_get.assert_called_with(stripped_lines)


    @patch("cdprocessing.functions.filter_float_groups")
    @patch("cdprocessing.functions.get_float_groups")
    def test_extractor_filters_float_groups(self, test_get, test_filter):
        test_get.return_value = [[[100, 200, 300]], [[279, 2, 3]]]
        test_filter.return_value = [[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]
        series = extract_all_series(self.single_scan_file)
        test_filter.assert_called_with(test_get.return_value)
        self.assertEqual(series, test_filter.return_value)



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



class FloatGroupFilterTests(ViewTest):

    def test_can_filter_zero_float_groups(self):
        self.assertEqual(filter_float_groups([]), [])


    def test_can_filter_out_small_float_groups(self):
        filtered_groups = filter_float_groups([
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


    def test_can_filter_float_groups_whose_wavelengths_dont_match(self):
        filtered_groups = filter_float_groups([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.7, 34, 1]]
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_can_filter_float_groups_with_fewer_than_3_values(self):
        filtered_groups = filter_float_groups([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74], [4.5, 1], [76.8, 4]]
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]]
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
