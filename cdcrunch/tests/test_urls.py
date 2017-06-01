from cdtool.tests import UrlTest
from cdcrunch import views

class CdcrunchUrlTests(UrlTest):

    def test_root_url_resolves_to_tool_page_view(self):
        self.check_url_returns_view("/", views.tool_page)
