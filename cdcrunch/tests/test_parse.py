from inferi import Dataset
from imagipy import Color
from unittest.mock import patch, Mock, MagicMock
from cdtool.tests import ViewTest
from cdcrunch.parse import *
from cdcrunch.exceptions import *

class FilesToSampleTests(ViewTest):

    @patch("cdcrunch.parse.files_to_one_component_sample")
    def test_can_convert_one_component_files(self, mock_sample):
        mock_sample.return_value = {"sample": "yes"}
        sample = files_to_sample([self.test_file1, self.test_file2], name="S")
        mock_sample.assert_called_with([self.test_file1, self.test_file2])
        self.assertEqual(sample, {"sample": "yes", "name": "S"})


    @patch("cdcrunch.parse.files_to_two_component_sample")
    def test_can_convert_two_component_files(self, mock_sample):
        mock_sample.return_value = {"sample": "yes"}
        sample = files_to_sample([self.test_file1], baseline=[self.test_file2], name="S")
        mock_sample.assert_called_with([self.test_file1], [self.test_file2])
        self.assertEqual(sample, {"sample": "yes", "name": "S"})



class FilesToOneComponentSampleTests(ViewTest):

    @patch("cdcrunch.parse.files_to_scans")
    def test_zero_scans(self, mock_scans):
        mock_scans.return_value = []
        with self.assertRaises(NoScansError):
            files_to_one_component_sample([self.test_file1, self.test_file2])


    @patch("cdcrunch.parse.files_to_scans")
    @patch("cdcrunch.parse.scan_to_dict")
    def test_one_scan(self, mock_dict, mock_scans):
        mock_scans.return_value = ["scan1"]
        mock_dict.return_value = {"sample": "yes"}
        sample = files_to_one_component_sample([self.test_file1, self.test_file2])
        mock_scans.assert_called_with([self.test_file1, self.test_file2])
        mock_dict.assert_called_with("scan1", linewidth=2, color="#16A085")
        self.assertEqual(sample, {"sample": "yes"})


    @patch("cdcrunch.parse.files_to_scans")
    @patch("cdcrunch.parse.generate_colors")
    @patch("cdcrunch.parse.scan_to_dict")
    @patch("cdcrunch.parse.average_scans")
    def test_multiple_scans(self, mock_avg, mock_dict, mock_col, mock_scans):
        mock_scans.return_value = ["scan1", "scan2"]
        mock_col.return_value = ["RED", "BLUE"]
        mock_dict.side_effect = [{"sample": "yes"}, {"sample": "1"}, {"sample": "2"}]
        mock_avg.return_value = "average_scan"
        sample = files_to_one_component_sample([self.test_file1, self.test_file2])
        mock_scans.assert_called_with([self.test_file1, self.test_file2])
        mock_avg.assert_called_with("scan1", "scan2")
        mock_dict.assert_any_call("average_scan", linewidth=2, color="#16A085")
        mock_col.assert_called_with(2)
        mock_dict.assert_any_call("scan1", linewidth=1, color="RED")
        mock_dict.assert_any_call("scan2", linewidth=1, color="BLUE")
        self.assertEqual(sample, {
         "sample": "yes", "scans": [{"sample": "1"}, {"sample": "2"}]
        })



class FilesToTwoComponentSampleTests(ViewTest):

    @patch("cdcrunch.parse.files_to_scans")
    def test_zero_scans(self, mock_scans):
        mock_scans.side_effect = [[], []]
        with self.assertRaises(NoScansError):
            files_to_two_component_sample([self.test_file1], [self.test_file2])


    @patch("cdcrunch.parse.files_to_scans")
    def test_zero_raw_scans(self, mock_scans):
        mock_scans.side_effect = [[], ["scan"]]
        with self.assertRaises(NoMinuendScansError):
            files_to_two_component_sample([self.test_file1], [self.test_file2])


    @patch("cdcrunch.parse.files_to_scans")
    def test_zero_baseline_scans(self, mock_scans):
        mock_scans.side_effect = [["scan"], []]
        with self.assertRaises(NoSubtrahendScansError):
            files_to_two_component_sample([self.test_file1], [self.test_file2])


    @patch("cdcrunch.parse.files_to_scans")
    @patch("cdcrunch.parse.subtract_components")
    @patch("cdcrunch.parse.scan_to_dict")
    def test_can_turn_one_raw_one_baseline_to_sample(self, mock_dict, mock_sub, mock_scans):
        mock_scans.side_effect = [["raw_scan"], ["baseline_scan"]]
        mock_sub.return_value = "subtracted"
        mock_dict.side_effect = [{"sample": "yes"}, {"sample": "r"}, {"sample": "b"}]
        sample = files_to_two_component_sample([self.test_file1], [self.test_file2])
        mock_scans.assert_any_call([self.test_file1])
        mock_scans.assert_any_call([self.test_file2])
        mock_sub.assert_called_with("raw_scan", "baseline_scan")
        mock_dict.assert_any_call("subtracted", linewidth=2, color="#16A085")
        mock_dict.assert_any_call("raw_scan", linewidth=1.5, color="#137864")
        mock_dict.assert_any_call("baseline_scan", linewidth=1.5, color="#A0D6FA")
        self.assertEqual(sample, {
         "sample": "yes", "components": [{"sample": "r"}, {"sample": "b"}]
        })



class FilesToScansTests(ViewTest):

    @patch("cdcrunch.parse.file_to_scans")
    def test_can_turn_files_to_no_scans(self, mock_scans):
        mock_scans.side_effect = [[], []]
        scans = files_to_scans(["file1", "file2"])
        mock_scans.assert_any_call("file1")
        mock_scans.assert_any_call("file2")
        self.assertEqual(scans, [])


    @patch("cdcrunch.parse.file_to_scans")
    def test_can_turn_files_to_scans(self, mock_scans):
        mock_scans.side_effect = [["scan1"], ["scan2", "scan3"]]
        scans = files_to_scans(["file1", "file2"])
        mock_scans.assert_any_call("file1")
        mock_scans.assert_any_call("file2")
        self.assertEqual(scans, ["scan1", "scan2", "scan3"])



class FileToScanTests(ViewTest):

    @patch("cdcrunch.parse.file_to_lines")
    @patch("cdcrunch.parse.extract_data_blocks")
    @patch("cdcrunch.parse.remove_short_data_blocks")
    @patch("cdcrunch.parse.remove_incorrect_wavelengths")
    @patch("cdcrunch.parse.remove_short_lines")
    @patch("cdcrunch.parse.strip_data_blocks")
    @patch("cdcrunch.parse.block_to_dataset")
    def test_can_file_to_scans(self, mock_data, mock_strip, mock_line, mock_wav,
                               mock_short, mock_blocks, mock_lines):
        mock_lines.return_value = ["line1", "line2", "line3"]
        mock_blocks.return_value = ["b1", "b2", "b3", "b4", "b5", "b6"]
        mock_short.return_value = ["b1", "b2", "b3", "b4", "b5"]
        mock_wav.return_value = ["b1", "b2", "b3", "b4"]
        mock_line.return_value = ["b1", "b2", "b3"]
        mock_strip.return_value = ["1", "2", "3"]
        dataset1, dataset2, dataset3 = Mock(), Mock(), Mock()
        mock_data.side_effect = [dataset1, dataset2, dataset3]
        scans = file_to_scans(self.test_file1)
        mock_lines.assert_called_with(self.test_file1)
        mock_blocks.assert_called_with(["line1", "line2", "line3"])
        mock_short.assert_called_with(["b1", "b2", "b3", "b4", "b5", "b6"])
        mock_wav.assert_called_with(["b1", "b2", "b3", "b4", "b5"])
        mock_line.assert_called_with(["b1", "b2", "b3", "b4"])
        mock_strip.assert_called_with(["b1", "b2", "b3"])
        mock_data.assert_any_call("1")
        mock_data.assert_any_call("2")
        mock_data.assert_any_call("3")
        self.assertEqual(scans, [dataset1, dataset2, dataset3])



class FileToLinesTests(ViewTest):

    def test_can_get_lines_from_file(self):
        lines = file_to_lines(self.test_file1)
        self.assertEqual(lines, [
         "$MDCDATA:1:14:2:3:4:9",
         "100 200 300",
         "X  CD_Signal  CD_Error  CD_Current_(Abs)",
         "279.000  1.0  0.5  1.013  -0.000  242.9  19.98",
         "278.000  -4.0  0.4  1.013  0.000  243.2  19.99",
         "277.000  12.0  0.3  1.013  0.000  243.5  19.99",
        ])


    def test_empty_list_returned_if_file_is_binary(self):
        lines = file_to_lines(self.binary_file)
        self.assertEqual(lines, [])



class DataBlockExtractionTests(ViewTest):

    def test_can_find_data_blocks(self):
        data_blocks = extract_data_blocks([
         "Irrelevant string1", "Irrelevant string2",
         "3 76 34", "4.5 4 32", "76.8 34 3",
         "More random data",
         "67.4 45", "45.6 4 4 4", "67.6 string", "7.4 7.4",
         "String 4"
        ])
        self.assertEqual(data_blocks, [
         [[3, 76, 34], [4.5, 4, 32], [76.8, 34, 3]],
         [[67.4, 45], [45.6, 4, 4, 4]],
         [[7.4, 7.4]]
        ])


    def test_can_get_zero_data_blocks(self):
        data_blocks = extract_data_blocks([
         "Irrelevant string1", "Irrelevant string2",
         "More random data", "67.6 string", "String 4"
        ])
        self.assertEqual(data_blocks, [])



class ShortDataBlockRemovalTests(ViewTest):

    def test_can_filter_zero_data_blocks(self):
        self.assertEqual(remove_short_data_blocks([]), [])


    def test_can_remove_short_groups(self):
        filtered_blocks = remove_short_data_blocks([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[67.4, 45, 1], [45.6, 4, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[7.4, 7.4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
        ])
        self.assertEqual(filtered_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]]
        ])



class IncorrectWavelengthRemovalTests(ViewTest):

    def test_can_filter_zero_data_blocks(self):
        self.assertEqual(remove_incorrect_wavelengths([]), [])


    def test_can_remove_incorrect_wavelengths(self):
        filtered_blocks = remove_incorrect_wavelengths([
         [[3, 76, 1], [4.5, 4, 1], [75.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(filtered_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])



class ShortLineRemovalTests(ViewTest):

    def test_can_filter_zero_data_blocks(self):
        self.assertEqual(remove_short_lines([]), [])


    def test_can_remove_short_lines(self):
        filtered_blocks = remove_short_lines([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76], [4.5, 4], [76.8, 34]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(filtered_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])



class BlockStrippingTests(ViewTest):

    def test_can_strip_zero_data_blocks(self):
        self.assertEqual(strip_data_blocks([]), [])


    @patch("cdcrunch.parse.is_possible_error_column")
    def test_three_column_blocks_with_valid_error_unchanged(self, mock_check):
        mock_check.return_value = True
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1], [4.5, 4, 0.5], [76.8, 34, 1.2]],
         [[3, 77, 0.9], [4.5, 3, 4], [76.8, 34, 1]],
         [[3, 74, 17], [4.5, 5, 18], [76.8, 4, 19]]
        ])
        mock_check.assert_called_with(
         [1, 0.5, 1.2, 0.9, 4, 1, 17, 18, 19],
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 0.5], [76.8, 34, 1.2]],
         [[3, 77, 0.9], [4.5, 3, 4], [76.8, 34, 1]],
         [[3, 74, 17], [4.5, 5, 18], [76.8, 4, 19]]
        ])


    @patch("cdcrunch.parse.is_possible_error_column")
    def test_three_column_blocks_with_invalid_error(self, mock_check):
        mock_check.return_value = False
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1], [4.5, 4, 0.5], [76.8, 34, 1.2]],
         [[3, 77, 0.9], [4.5, 3, 4], [76.8, 34, 1]],
         [[3, 74, 17], [4.5, 5, 18], [76.8, 4, 19]]
        ])
        mock_check.assert_called_with(
         [1, 0.5, 1.2, 0.9, 4, 1, 17, 18, 19],
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        self.assertEqual(stripped_blocks, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 77, 0], [4.5, 3, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])


    @patch("cdcrunch.parse.is_possible_error_column")
    def test_first_valid_column_used(self, mock_check):
        mock_check.return_value = True
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 9], [4.5, 4, 0.5, 9], [76.8, 34, 1.2, 9]],
         [[3, 77, 0.9, 9], [4.5, 3, 4, 9], [76.8, 34, 1, 9]],
         [[3, 74, 17, 9], [4.5, 5, 18, 9], [76.8, 4, 19, 9]]
        ])
        mock_check.assert_any_call(
         [1, 0.5, 1.2, 0.9, 4, 1, 17, 18, 19],
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        mock_check.assert_any_call(
         [9] * 9,
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 0.5], [76.8, 34, 1.2]],
         [[3, 77, 0.9], [4.5, 3, 4], [76.8, 34, 1]],
         [[3, 74, 17], [4.5, 5, 18], [76.8, 4, 19]]
        ])


    @patch("cdcrunch.parse.is_possible_error_column")
    def test_can_skip_columns(self, mock_check):
        mock_check.side_effect = [False, True]
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 9], [4.5, 4, 0.5, 9], [76.8, 34, 1.2, 9]],
         [[3, 77, 0.9, 9], [4.5, 3, 4, 9], [76.8, 34, 1, 9]],
         [[3, 74, 17, 9], [4.5, 5, 18, 9], [76.8, 4, 19, 9]]
        ])
        mock_check.assert_any_call(
         [1, 0.5, 1.2, 0.9, 4, 1, 17, 18, 19],
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        mock_check.assert_any_call(
         [9] * 9,
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        self.assertEqual(stripped_blocks, [
         [[3, 76, 9], [4.5, 4, 9], [76.8, 34, 9]],
         [[3, 77, 9], [4.5, 3, 9], [76.8, 34, 9]],
         [[3, 74, 9], [4.5, 5, 9], [76.8, 4, 9]]
        ])


    @patch("cdcrunch.parse.is_possible_error_column")
    def test_can_discard_all_columns(self, mock_check):
        mock_check.return_value = False
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 9], [4.5, 4, 0.5, 9], [76.8, 34, 1.2, 9]],
         [[3, 77, 0.9, 9], [4.5, 3, 4, 9], [76.8, 34, 1, 9]],
         [[3, 74, 17, 9], [4.5, 5, 18, 9], [76.8, 4, 19, 9]]
        ])
        mock_check.assert_any_call(
         [1, 0.5, 1.2, 0.9, 4, 1, 17, 18, 19],
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        mock_check.assert_any_call(
         [9] * 9,
         [76, 4, 34, 77, 3, 34, 74, 5, 4]
        )
        self.assertEqual(stripped_blocks, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 77, 0], [4.5, 3, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])



class ErrorColumnValidationTests(ViewTest):

    def test_discarding_of_negative_columns(self):
        self.assertFalse(is_possible_error_column(
         [0.6, 0.4, 0.3, -0.1, 0.6], [12, 13, 11, 9, 12]
        ))
        self.assertTrue(is_possible_error_column(
         [0.6, 0.4, 0.3, 0.1, 0.6], [12, 13, 11, 9, 12]
        ))


    def test_discarding_of_all_zero_columns(self):
        self.assertFalse(is_possible_error_column(
         [0, 0, 0, 0, 0], [12, 13, 11, 9, 12]
        ))
        self.assertTrue(is_possible_error_column(
         [0, 0, 0, 1, 0], [12, 13, 11, 9, 12]
        ))


    def test_discarding_of_too_large_values(self):
        self.assertFalse(is_possible_error_column(
         [0.6, 0.4, 0.3, 1.8, 0.6], [0.1, 0.6, -0.3, 0.01, -0.2]
        ))
        self.assertTrue(is_possible_error_column(
         [0.6, 0.4, 0.3, 1.7, 0.6], [0.1, 0.6, -0.3, 0.01, -0.2]
        ))



class BlockToDatasetTests(ViewTest):

    def test_can_convert_block_to_dataset(self):
        block = [[3, 76, 1], [4.5, 4, 2], [76.8, 34, 3]]
        dataset = block_to_dataset(block)
        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(len(dataset.variables()), 2)
        self.assertEqual(dataset.variables()[0].values(), (3, 4.5, 76.8))
        self.assertEqual(dataset.variables()[0].error(), (0, 0, 0))
        self.assertEqual(dataset.variables()[1].values(), (76, 4, 34))
        self.assertEqual(dataset.variables()[1].error(), (1, 2, 3))



class ColorGenerationTests(ViewTest):

    def test_can_get_all_imagipy_colors(self):
        colors = generate_colors(6)
        self.assertEqual(colors, [
         Color.RED.hex(), Color.BLUE.hex(), Color.ORANGE.hex(),
         Color.PURPLE.hex(), Color.GREEN.hex(), Color.BROWN.hex()
        ])


    def test_can_get_some_imagipy_colors(self):
        colors = generate_colors(2)
        self.assertEqual(colors, [Color.RED.hex(), Color.BLUE.hex()])


    @patch("cdcrunch.parse.Color.mutate")
    def test_can_get_variants_on_imaginary_colors(self, mock_mutate):
        mutated_colors = [Mock(Color) for _ in range(6)]
        for color in mutated_colors:
            color.hex.return_value = color
        mock_mutate.side_effect = mutated_colors
        colors = generate_colors(12)
        self.assertEqual(colors, [
         Color.RED.hex(), Color.BLUE.hex(), Color.ORANGE.hex(),
         Color.PURPLE.hex(), Color.GREEN.hex(), Color.BROWN.hex(),
         *mutated_colors
        ])



class DatasetAveragingTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.wav1, self.wav2 = Mock(Variable), Mock(Variable)
        self.cd1, self.cd2 = Mock(Variable), Mock(Variable)
        self.wav1.length.return_value = self.cd1.length.return_value = 5
        self.wav2.length.return_value = self.cd2.length.return_value = 5
        self.dataset1 = Dataset(self.wav1, self.cd1)
        self.dataset2 = Dataset(self.wav2, self.cd2)


    @patch("cdcrunch.parse.Variable.average")
    def test_can_average_scans(self, mock_average):
        averaged_cd = Mock(Variable)
        averaged_cd.length.return_value = 5
        mock_average.return_value = averaged_cd
        average = average_scans(self.dataset1, self.dataset2)
        self.assertIsInstance(average, Dataset)
        mock_average.assert_called_with(self.cd1, self.cd2, sd_err=True)
        self.assertEqual(len(average.variables()), 2)
        self.assertIs(average.variables()[0], self.wav1)
        self.assertIs(average.variables()[1], averaged_cd)



class DatasetSubtractionTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.wav1, self.wav2 = Mock(Variable), Mock(Variable)
        self.cd1, self.cd2 = Mock(Variable), Mock(Variable)
        self.wav1.length.return_value = self.cd1.length.return_value = 5
        self.wav2.length.return_value = self.cd2.length.return_value = 5
        self.dataset1 = Dataset(self.wav1, self.cd1)
        self.dataset2 = Dataset(self.wav2, self.cd2)


    @patch("cdcrunch.parse.Variable.__sub__")
    def test_can_subtract_scans(self, mock_sub):
        subtracted_cd = Mock(Variable)
        subtracted_cd.length.return_value = 5
        self.cd1.__sub__ = MagicMock()
        self.cd1.__sub__.return_value = subtracted_cd
        sub = subtract_components(self.dataset1, self.dataset2)
        self.assertIsInstance(sub, Dataset)
        self.cd1.__sub__.assert_called_with(self.cd2)
        self.assertEqual(len(sub.variables()), 2)
        self.assertIs(sub.variables()[0], self.wav1)
        self.assertIs(sub.variables()[1], subtracted_cd)



class ScanToDictTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        wav = Variable(180, 179, 178)
        cd = Variable(1, -1, 4, error=[0.5, 1.1, 0.2])
        self.scan = Dataset(wav, cd)


    def test_can_convert_scan_to_dict(self):
        json = scan_to_dict(self.scan)
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 1,
         "color": "#000000",
         "scans": [],
         "components": []
        })


    def test_can_set_linewidth(self):
        json = scan_to_dict(self.scan, linewidth=2)
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 2,
         "color": "#000000",
         "scans": [],
         "components": []
        })


    def test_can_set_color(self):
        json = scan_to_dict(self.scan, color="#FF00FF")
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 1,
         "color": "#FF00FF",
         "scans": [],
         "components": []
        })
