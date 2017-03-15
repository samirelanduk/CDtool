from django.test import TestCase
from cdprocessing.functions import clean_file

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
