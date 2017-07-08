import inferi
from unittest.mock import patch, Mock
from cdtool.tests import ViewTest
from cdcrunch.parse import *

class AllScanExtractionFromFileTests(ViewTest):

    @patch("cdcrunch.parse.get_data_blocks")
    @patch("cdcrunch.parse.remove_short_data_blocks")
    @patch("cdcrunch.parse.remove_incorrect_wavelengths")
    @patch("cdcrunch.parse.remove_short_lines")
    @patch("cdcrunch.parse.strip_data_blocks")
    @patch("cdcrunch.parse.block_to_variables")
    def test_extractor_calls_correct_functions(self, *mocks):
        data_blocks = Mock()
        len_filtered_data_blocks = Mock()
        wav_filtered_data_blocks = Mock()
        line_filtered_data_blocks = Mock()
        stripped_data_blocks = [Mock(), Mock(), Mock()]
        (mock_variables, mock_strip, mock_line_filter, mock_wav_filter,
         mock_len_filter, mock_get) = mocks
        mock_get.return_value = data_blocks
        mock_len_filter.return_value = len_filtered_data_blocks
        mock_wav_filter.return_value = wav_filtered_data_blocks
        mock_line_filter.return_value = line_filtered_data_blocks
        mock_strip.return_value = stripped_data_blocks

        mock_variables.return_value = Mock()
        series = extract_all_scans(self.test_file)
        stripped_lines = [
         "$MDCDATA:1:14:2:3:4:9",
         "100 200 300",
         "X  CD_Signal  CD_Error  CD_Current_(Abs)",
         "279.000  1.0  0.5  1.013  -0.000  242.9  19.98",
         "278.000  -4.0  0.4  1.013  0.000  243.2  19.99",
         "277.000  12.0  0.3  1.013  0.000  243.5  19.99"
        ]
        mock_get.assert_called_with(stripped_lines)
        mock_len_filter.assert_called_with(data_blocks)
        mock_wav_filter.assert_called_with(len_filtered_data_blocks)
        mock_line_filter.assert_called_with(wav_filtered_data_blocks)
        mock_strip.assert_called_with(line_filtered_data_blocks)
        for block in mock_strip.return_value:
            mock_variables.assert_any_call(block)
        self.assertEqual(series, [mock_variables.return_value] * 3)



class DataGrouperTests(ViewTest):

    def test_can_find_data_blocks(self):
        data_blocks = get_data_blocks([
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
        self.assertEqual(data_blocks, [
         [[3, 76, 34], [4.5, 4, 32], [76.8, 34, 3]],
         [[67.4, 45], [45.6, 4, 4, 4]],
         [[7.4, 7.4]]
        ])


    def test_data_blocks_returns_nothing_if_no_data_blocks(self):
        data_blocks = get_data_blocks([
         "Irrelevant string1",
         "Irrelevant string2",
         "More random data",
         "67.6 string",
         "String 4"
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



class DataBlockStrippingTests(ViewTest):

    def test_can_strip_zero_data_blocks(self):
        self.assertEqual(strip_data_blocks([]), [])


    def test_stripping_len_3_lines_does_nothing(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_just_uses_3_values_per_line(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 10], [4.5, 4, 1, 11], [76.8, 34, 1, 10]],
         [[3, 76, 1, 9], [4.5, 4, 1, 3], [76.8, 34, 1, 8]],
         [[3, 74, 1, 2], [4.5, 5, 1, 4], [76.8, 4, 1, 5]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_negative_columns(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, -1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, -1, 1]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_100_columns(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, 101, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, 101, 1]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_discards_columns_that_are_entirely_zero(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 0, 0, 1], [4.5, 4, 0, 0, 1], [76.8, 34, 0, 0, 1]],
         [[3, 76, 0, 0, 1], [4.5, 4, 0, 0, 1], [76.8, 34, 0, 0, 1]],
         [[3, 74, 0, 0, 1], [4.5, 5, 0, 0, 1], [76.8, 4, 0, 0, 1]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 76, 1], [4.5, 4, 1], [76.8, 34, 1]],
         [[3, 74, 1], [4.5, 5, 1], [76.8, 4, 1]]
        ])


    def test_stripping_handles_running_out_of_columns(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 1, 1, 1], [4.5, 4, 1, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 76, 1, 1, 1], [4.5, 4, 101, 1, 1], [76.8, 34, 1, 1, 1]],
         [[3, 74, 1, 1, 1], [4.5, 5, 1, 1, 1], [76.8, 4, 1, 101, -1]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])


    def test_stripping_handles_all_zeroes_columns(self):
        stripped_blocks = strip_data_blocks([
         [[3, 76, 0, 0, 0], [4.5, 4, 0, 0, 0], [76.8, 34, 0, 0, 0]],
         [[3, 76, 0, 0, 0], [4.5, 4, 0, 0, 0], [76.8, 34, 0, 0, 0]],
         [[3, 74, 0, 0, 0], [4.5, 5, 0, 0, 0], [76.8, 4, 0, 0, 0]]
        ])
        self.assertEqual(stripped_blocks, [
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 76, 0], [4.5, 4, 0], [76.8, 34, 0]],
         [[3, 74, 0], [4.5, 5, 0], [76.8, 4, 0]]
        ])



class DataBlockToInferiVariablesTests(ViewTest):

    def test_can_convert_data_block_to_inferi_variables(self):
        inferi_variables = block_to_variables([
         [3, 76, 1.2], [4.5, 4, 0.34], [76.8, 34, 0.9]
        ])
        wavelength, cd = inferi_variables
        self.assertIsInstance(wavelength, inferi.Variable)
        self.assertEqual(wavelength.name(), "wavelength")
        self.assertEqual(wavelength.values(), (3, 4.5, 76.8))
        self.assertEqual(wavelength.error(), (0, 0, 0))
        self.assertIsInstance(cd, inferi.Variable)
        self.assertEqual(cd.name(), "cd")
        self.assertEqual(cd.values(), (76, 4, 34))
        self.assertEqual(cd.error(), (1.2, 0.34, 0.9))
