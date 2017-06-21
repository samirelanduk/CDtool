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
