from django.test import TestCase
from cdcrunch.parse import *

class DataGrouperTests(TestCase):

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



class ShortDataBlockRemovalTests(TestCase):

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



class IncorrectWavelengthRemovalTests(TestCase):

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



class ShortLineRemovalTests(TestCase):

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



class DataBlockStrippingTests(TestCase):

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
