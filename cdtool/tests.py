from django.core.urlresolvers import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)



class ViewTest(TestCase):

    def setUp(self):
        self.single_scan_file = SimpleUploadedFile(
         "single_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  -0.006  0.083  1.013  -0.000  242.9  19.98
         278.000  0.044  0.148  1.013  0.000  243.2  19.99
         277.000  0.031  0.119  1.013  0.000  243.5  19.99
         276.000  -0.158  0.031  1.013  -0.002  244.0  19.98
         275.000  -0.151  0.144  1.013  -0.002  244.2  19.99"""
        )

        self.multi_scan_file = SimpleUploadedFile(
         "multi_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  -0.006  0.083  1.013  -0.000  242.9  19.98
         278.000  0.042  0.148  1.013  0.000  243.2  19.99
         277.000  0.036  0.119  1.013  0.000  243.5  19.99
         276.000  -0.158  0.031  1.013  -0.002  244.0  19.98
         275.000  -0.151  0.144  1.013  -0.002  244.2  19.99
         $MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  -0.047  0.067  1.013  -0.000  242.9  19.99
         278.000  0.040  0.188  1.013  0.000  243.3  19.99
         277.000  -0.275  0.197  1.013  -0.003  243.5  19.99
         276.000  0.116  0.132  1.013  0.001  243.9  19.98
         275.000  0.154  0.053  1.013  0.002  244.2  19.99"""
        )
