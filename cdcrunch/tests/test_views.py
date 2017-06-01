from cdtool.tests import ViewTest

class ToolPageViewTests(ViewTest):

    def test_tool_view_uses_tool_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "tool.html")
