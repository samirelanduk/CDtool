from django.core.urlresolvers import resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

class UrlTest(TestCase):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)



class ViewTest(TestCase):

    def setUp(self):
        self.test_file = SimpleUploadedFile(
         "single_scan.dat",
         b"""$MDCDATA:1:14:2:3:4:9
         100 200 300
          X  CD_Signal  CD_Error  CD_Current_(Abs)
         279.000  1.0  0.5  1.013  -0.000  242.9  19.98
         278.000  -4.0  0.4  1.013  0.000  243.2  19.99
         277.000  12.0  0.3  1.013  0.000  243.5  19.99"""
        )

        self.sample = {
         "name": "",
         "values": [],
         "error": [],
         "color": "#4A9586",
         "width": 1.5,
         "raw": {},
         "baseline": {}
        }
