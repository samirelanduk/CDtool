from inferi import Variable
from unittest.mock import patch
from cdtool.tests import ViewTest

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
