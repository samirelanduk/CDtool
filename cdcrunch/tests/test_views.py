from inferi import Variable
from datetime import datetime
from unittest.mock import patch, Mock
from django.http.response import HttpResponse
from cdtool import version
from cdtool.tests import ViewTest
from cdcrunch.views import produce_filename

class ToolPageViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.patcher = patch("cdcrunch.parse.extract_all_scans")
        self.mock_extract = self.patcher.start()
        self.mock_extract.return_value = [
         [Variable(172, 173, 174), Variable(12, 13, 11, error=[0.2, 0.4, 0.3])]
        ]


    def tearDown(self):
        self.patcher.stop()


    def test_tool_view_uses_tool_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "tool.html")


    @patch("cdcrunch.views.download_view")
    def test_request_is_forwarded_to_download_view_on_right_post(self, mock_view):
        mock_response = HttpResponse()
        mock_view.return_value = mock_response
        response = self.client.post("/", data={"series": [1]})
        self.assertIs(response, mock_response)


    def test_tool_displays_chart_on_post(self):
        response = self.client.post("/", data={"raw-files": self.test_file})
        self.assertTrue(response.context["output"])


    def test_tool_sends_title(self):
        response = self.client.post("/", data={
         "exp-name": "Title", "raw-files": self.test_file
        })
        self.assertEqual(response.context["title"], "Title")


    def test_tool_sends_x_limits(self):
        response = self.client.post("/", data={"raw-files": self.test_file})
        self.assertEqual(response.context["x_min"], 172)
        self.assertEqual(response.context["x_max"], 174)


    def test_tool_sends_data_object(self):
        self.sample["values"] = [[172, 12], [173, 13], [174, 11]]
        self.sample["errors"] = [[172, 11.8, 12.2], [173, 12.6, 13.4], [174, 10.7, 11.3]]
        self.sample["name"] = "Test Sample"
        response = self.client.post("/", data={
         "raw-files": self.test_file, "sample-name": "Test Sample"
        })
        self.assertEqual(response.context["data"], [self.sample])


    def test_tool_sends_file_series(self):
        response = self.client.post("/", data={"raw-files": self.test_file})
        self.assertEqual(response.context["file_series"], [
         [174, 11, 0.3], [173, 13, 0.4], [172, 12, 0.2],
        ])


    def test_tool_sends_error_if_no_files_given(self):
        response = self.client.post("/")
        self.assertIn("didn't submiy any files", response.context["error_text"])



class DownloadViewTests(ViewTest):

    def test_download_view_sends_file_if_series_given(self):
        response = self.client.post("/", data={
         "series": "[]",
         "name": "test"
        })
        self.assertEqual(response["Content-Type"], "application/plain-text")


    @patch("cdcrunch.views.produce_filename")
    def test_download_view_sends_file_returned_with_the_name_given(self, mock_name):
        mock_name.return_value = "TEST.DAT"
        response = self.client.post("/", data={
         "series": "[]",
         "name": "test"
        })
        mock_name.assert_called_with("test")
        self.assertIn("TEST.DAT", response["Content-Disposition"])


    def test_assert_file_produced_has_current_version(self):
        response = self.client.post("/", data={
         "series": "[]",
         "name": "test"
        })
        self.assertContains(response, version)


    def test_file_returned_uses_current_date(self):
        response = self.client.post("/", data={
         "series": "[]",
         "name": "test"
        })
        self.assertContains(response, datetime.now().strftime("%Y"))
        self.assertContains(response, datetime.now().strftime("%B"))
        self.assertContains(response, datetime.now().strftime("%A"))


    def test_file_returned_has_provided_series(self):
        response = self.client.post("/", data={
         "series": "[[280.0, 0.17, 0.1], [279.0, 0.99, 0.2], [278.0, 0.2, 0.3]]",
         "name": "test"
        })
        lines = response.content.decode().split("\n")
        self.assertEqual(
         [float(value) for value in lines[-3].split()],
         [280, 0.17, 0.1]
        )
        self.assertEqual(
         [float(value) for value in lines[-2].split()],
         [279, 0.99, 0.2]
        )
        self.assertEqual(
         [float(value) for value in lines[-1].split()],
         [278, 0.2, 0.3]
        )



class FileNameProductionTests(ViewTest):

    def test_can_append_dat(self):
        self.assertEqual(produce_filename("string"), "string.dat")


    def test_can_replace_spaces(self):
        self.assertEqual(produce_filename("str ing"), "str_ing.dat")


    def test_can_go_to_lower_case(self):
        self.assertEqual(produce_filename("String"), "string.dat")


    def test_invalid_characters_replaced(self):
        self.assertEqual(produce_filename("s:trin@g"), "s-trin-g.dat")
