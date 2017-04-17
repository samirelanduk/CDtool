from django.core.urlresolvers import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)



class ViewTest(TestCase):

    def setUp(self):
        self.no_scan_file = SimpleUploadedFile(
         "single_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
          """
        )

        self.single_scan_file = SimpleUploadedFile(
         "single_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
         100 200 300
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  1.0  0.5  1.013  -0.000  242.9  19.98
         278.000  -4.0  0.4  1.013  0.000  243.2  19.99
         277.000  12.0  0.3  1.013  0.000  243.5  19.99"""
        )

        self.multi_scan_file = SimpleUploadedFile(
         "multi_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
         100 200 300
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  1.0  0.5  1.013  -0.000  242.9  19.98
         278.000  -4.0  0.4  1.013  0.000  243.2  19.99
         277.000  12.0  0.3  1.013  0.000  243.5  19.99
         $MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  0.0  0.2  1.013  -0.000  242.9  19.99
         278.000  -5.0  0.75  1.013  0.000  243.3  19.99
         277.000  11.0  0.4  1.013  -0.003  243.5  19.99
         $MDCDATA:1:14:2:3:4:9
          X  CD_Signal  CD_Error  CD_Current_(Abs)  CD_Delta_Absorbance  CD_Dynode  Jacket_Temp.
         279.000  2.0  0.1  1.013  -0.000  242.9  19.99
         278.000  -3.0  0.3  1.013  0.000  243.3  19.99
         277.000  13.0  0.2  1.013  -0.003  243.5  19.99"""
        )
