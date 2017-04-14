from cdtool.tests import ViewTest
from cdprocessing.functions import extract_all_series, get_float_groups
from cdprocessing.functions import filter_float_groups, average_series

class AllSeriesExtractionFromFileTests(ViewTest):

    def test_can_pull_out_single_series_from_single_scan_file(self):
        series = extract_all_series(self.single_scan_file)
        self.assertEqual(series, [[
         [279, -0.006, 0.083], [278, 0.044, 0.148], [277, 0.031, 0.119]
        ]])


    def test_can_pull_out_multiple_series_from_multi_scan_file(self):
        series = extract_all_series(self.multi_scan_file)
        self.assertEqual(series, [
         [[279, -0.006, 0.083], [278, 0.042, 0.148], [277, 0.036, 0.119]],
         [[279, -0.047, 0.067], [278, 0.04, 0.188], [277, -0.275, 0.197]],
         [[279, -0.34, 0.067], [278, 0.01, 0.188], [277, -0.18, 0.197]]
        ])



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



class FloatGroupFilterTests(ViewTest):

    def test_can_filter_out_small_float_groups(self):
        filtered_groups = filter_float_groups([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[67.4, 45, 1], [45.6, 4, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[7.4, 7.4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.7, 34, 1]],
        ])
        self.assertEqual(filtered_groups, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
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
         [[279, -0.006, 0], [278, 0.042, 0], [277, 0.036, ]],
         [[279, -0.047], [278, 0.04], [277, -0.275]],
         [[279, -0.34], [278, 0.01], [277, -0.18]]
        ])
        self.assertEqual(len(average), 3)
        self.assertEqual(average[0][0], 279)
        self.assertEqual(average[1][0], 278)
        self.assertEqual(average[2][0], 277)
        self.assertAlmostEqual(average[0][1], -0.131, delta=0.005)
        self.assertAlmostEqual(average[1][1], 0.0307, delta=0.005)
        self.assertAlmostEqual(average[2][1], -0.1397, delta=0.005)
        self.assertAlmostEqual(average[0][2], 0.105, delta=0.005)
        self.assertAlmostEqual(average[1][2], 0.0103, delta=0.005)
        self.assertAlmostEqual(average[2][2], 0.092, delta=0.005)
