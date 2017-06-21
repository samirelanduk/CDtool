from django.test import TestCase
from cdcrunch.parse import get_data_blocks

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


    def test_data_blocks_returns_nothing_if_no_float_groups(self):
        data_blocks = get_data_blocks([
         "Irrelevant string1",
         "Irrelevant string2",
         "More random data",
         "67.6 string",
         "String 4"
        ])
        self.assertEqual(data_blocks, [])
