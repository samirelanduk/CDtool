from inferi import Variable
from datetime import datetime
from unittest.mock import patch, Mock
from django.http.response import HttpResponse
from cdtool import version
from cdtool.tests import ViewTest

class RootViewTests(ViewTest):

    @patch("cdcrunch.views.root_post")
    def test_root_view_uses_post_view_on_post(self, mock_view):
        mock_response = HttpResponse()
        mock_view.return_value = mock_response
        response = self.client.post("/")
        self.assertIs(response, mock_response)


    @patch("cdcrunch.views.root_get")
    def test_root_view_uses_get_view_on_get(self, mock_view):
        mock_response = HttpResponse()
        mock_view.return_value = mock_response
        response = self.client.get("/")
        self.assertIs(response, mock_response)



class RootGetViewTests(ViewTest):

    def test_get_view_returns_tool_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "tool.html")



class RootPostViewTests(ViewTest):

    @patch("cdcrunch.views.root_download")
    def test_post_view_sends_to_file_view_if_series_given(self, mock_view):
        mock_response = HttpResponse()
        mock_view.return_value = mock_response
        response = self.client.post("/", data={"series": "..."})
        self.assertIs(response, mock_response)


    @patch("cdcrunch.views.root_parse")
    def test_post_view_sends_to_parse_view_if_no_series_given(self, mock_view):
        mock_response = HttpResponse()
        mock_view.return_value = mock_response
        response = self.client.post("/")
        self.assertIs(response, mock_response)



class RootParseViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.data = {
         "raw-files": [self.test_file1, self.test_file2],
         "exp-name": "Title", "sample-name": "SS"
        }
        self.patcher = patch("cdcrunch.parse.files_to_sample")
        self.mock_sample = self.patcher.start()
        self.mock_sample.return_value = {"sample": "yes"}


    def tearDown(self):
        self.patcher.stop()


    def test_parse_view_returns_tool_template(self):
        response = self.client.post("/", data=self.data)
        self.assertTemplateUsed(response, "tool.html")


    def test_parse_view_displays_chart(self):
        response = self.client.post("/", data=self.data)
        self.assertTrue(response.context["output"])


    def test_parse_view_sends_title(self):
        response = self.client.post("/", data=self.data)
        self.assertEqual(response.context["title"], "Title")


    def test_error_on_no_file_sent(self):
        self.data["raw-files"] = ""
        response = self.client.post("/", data=self.data)
        self.assertIn("didn't submit any files", response.context["error_text"])


    def test_parse_view_sends_sample(self):
        response = self.client.post("/", data=self.data)
        args, kwargs = self.mock_sample.call_args_list[0]
        self.assertIsInstance(args[0], list)
        self.assertEqual(len(args[0]), 2)
        self.assertEqual(str(args[0][0]), "single_scan.dat")
        self.assertEqual(str(args[0][1]), "single_scan_two.dat")
        self.assertEqual(kwargs, {"name": "SS"})
        self.assertEqual(response.context["sample"], {"sample": "yes"})


    def test_error_on_no_scans_in_file(self):
        self.mock_sample.return_value = None
        response = self.client.post("/", data=self.data)
        self.assertIn("no scans", response.context["error_text"])



class RootDownloadViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.data = {"series": str({
         "series": [[190.0, 2.158], [191.0, 1.372], [192.0, 1.171]],
         "error": [[190.0, 1.8, 2.5], [191.0, 1.0, 1.7], [192.0, 0.8, 1.5]]
        }), "name": "Experiment Name"}


    @patch("cdcrunch.downloads.produce_filename")
    @patch("cdcrunch.downloads.series_to_file")
    def test_download_view_sends_file(self, mock_file, mock_name):
        response = self.client.post("/", data=self.data)
        self.assertEqual(response["Content-Type"], "application/plain-text")


    @patch("cdcrunch.downloads.produce_filename")
    @patch("cdcrunch.downloads.series_to_file")
    def test_download_view_sends_file_name_given(self, mock_file, mock_name):
        mock_name.return_value = "TEST.DAT"
        response = self.client.post("/", data=self.data)
        mock_name.assert_called_with("Experiment Name")
        self.assertIn("TEST.DAT", response["Content-Disposition"])


    @patch("cdcrunch.downloads.produce_filename")
    @patch("cdcrunch.downloads.series_to_file")
    def test_download_view_file_has_correct_text(self, mock_file, mock_name):
        mock_file.return_value = "FILEBODY"
        response = self.client.post("/", data=self.data)
        mock_file.assert_called_with(self.data["series"])
        self.assertContains(response, "FILEBODY")
