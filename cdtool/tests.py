from fuzz import Value
from django.core.urlresolvers import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)



class ViewTest(TestCase):

    def setUp(self):
        self.test_file1 = SimpleUploadedFile(
         "single_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
         100 200 300
          X  CD_Signal  CD_Error  CD_Current_(Abs)
         279.000  1.0  0.5  1.013  -0.000  242.9  19.98
         278.000  -4.0  0.4  1.013  0.000  243.2  19.99
         277.000  12.0  0.3  1.013  0.000  243.5  19.99

         """
        )

        self.test_file2 = SimpleUploadedFile(
         "single_scan_two.dat",
         b"""$MDCDATA:1:14:2:3:4:9
         400 100 900
          X  CD_Signal  CD_Error  CD_Current_(Abs)
         279.000  1.1  0.5  1.013  -0.000  241.9  19.98
         278.000  -4.0  0.4  1.013  0.000  243.2  19.99
         277.000  12.5  0.3  1.014  0.000  243.5  19.99

         """
        )

        self.binary_file = SimpleUploadedFile(
         "binary.dat", b"\xfc"
        )

        self.sample = {
         "name": "",
         "values": [],
         "errors": [],
         "scans": [],
         "color": "#4A9586",
         "width": 1.5,
         "raw": {},
         "baseline": {}
        }


    def check_data_equal(self, data1, data2):
        # Check no fuzz values
        self.assertNotIn("±", str(data1))
        self.assertNotIn("±", str(data2))

        # Same number of samples
        self.assertEqual(len(data1), len(data2))

        # Samples equal
        for sample1, sample2 in zip(data1, data2):
            # Sample attributes equal
            self.assertEqual(sample1["name"], sample2["name"])
            self.assertEqual(sample1["color"], sample2["color"])
            self.assertEqual(sample1["width"], sample2["width"])

            # Sample values and error equal
            self.assertEqual(len(sample1["values"]), len(sample2["values"]))
            self.assertEqual(len(sample1["errors"]), len(sample2["errors"]))
            for value1, value2 in zip(sample1["values"], sample2["values"]):
                self.assertEqual(value1[0], value2[0])
                self.assertAlmostEqual(value1[1], value2[1], delta=0.005)
            for error1, error2 in zip(sample1["errors"], sample2["errors"]):
                self.assertEqual(error1[0], error2[0])
                self.assertAlmostEqual(error1[1], error2[1], delta=0.005)
                self.assertAlmostEqual(error1[2], error2[2], delta=0.005)

            # Sample scans equal
            self.assertEqual(len(sample1["scans"]), len(sample2["scans"]))
            for scan1, scan2 in zip(sample1["scans"], sample2["scans"]):
                self.assertEqual(scan1["color"], scan2["color"])
                self.assertEqual(scan1["width"], scan2["width"])
                self.assertEqual(len(scan1["values"]), len(scan2["values"]))
                self.assertEqual(len(scan1["errors"]), len(scan2["errors"]))
                for value1, value2 in zip(scan1["values"], scan2["values"]):
                    self.assertEqual(value1[0], value2[0])
                    self.assertAlmostEqual(value1[1], value2[1], delta=0.005)
                for error1, error2 in zip(scan1["errors"], scan2["errors"]):
                    self.assertEqual(error1[0], error2[0])
                    self.assertAlmostEqual(error1[1], error2[1], delta=0.005)
                    self.assertAlmostEqual(error1[2], error2[2], delta=0.005)
