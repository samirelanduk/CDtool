from inferi import Dataset
from unittest.mock import patch, Mock
from cdtool.tests import ViewTest
from cdcrunch.parse import *

class ScanExtractionTests(ViewTest):

    @patch("cdcrunch.parse.file_to_lines")
    @patch("cdcrunch.parse.extract_data_blocks")
    @patch("cdcrunch.parse.remove_short_data_blocks")
    @patch("cdcrunch.parse.remove_incorrect_wavelengths")
    @patch("cdcrunch.parse.remove_short_lines")
    @patch("cdcrunch.parse.strip_data_blocks")
    @patch("cdcrunch.parse.block_to_dataset")
    def test_can_extract_scans(self, mock_data, mock_strip, mock_line, mock_wav,
                               mock_short, mock_blocks, mock_lines):
        mock_lines.return_value = ["line1", "line2", "line3"]
        mock_blocks.return_value = ["b1", "b2", "b3", "b4", "b5", "b6"]
        mock_short.return_value = ["b1", "b2", "b3", "b4", "b5"]
        mock_wav.return_value = ["b1", "b2", "b3", "b4"]
        mock_line.return_value = ["b1", "b2", "b3"]
        mock_strip.return_value = ["1", "2", "3"]
        dataset1, dataset2, dataset3 = Mock(), Mock(), Mock()
        mock_data.side_effect = [dataset1, dataset2, dataset3]
        scans = extract_scans(self.test_file)
        mock_lines.assert_called_with(self.test_file)
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
        lines = file_to_lines(self.test_file)
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



class DatasetToDictTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        wav = Variable(180, 179, 178)
        cd = Variable(1, -1, 4, error=[0.5, 1.1, 0.2])
        self.dataset = Dataset(wav, cd)


    def test_can_convert_dataset_to_dict(self):
        json = dataset_to_dict(self.dataset)
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 1,
         "color": "#000000",
         "name": ""
        })


    def test_can_set_linewidth(self):
        json = dataset_to_dict(self.dataset, linewidth=2)
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 2,
         "color": "#000000",
         "name": ""
        })


    def test_can_set_color(self):
        json = dataset_to_dict(self.dataset, color="#FF00FF")
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 1,
         "color": "#FF00FF",
         "name": ""
        })


    def test_can_set_color(self):
        json = dataset_to_dict(self.dataset, name="Samplename")
        self.assertEqual(json, {
         "series": [[178, 4], [179, -1], [180, 1]],
         "error": [[178, 3.8, 4.2], [179, -2.1, 0.1], [180, 0.5, 1.5]],
         "linewidth": 1,
         "color": "#000000",
         "name": "Samplename"
        })
