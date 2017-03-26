from cdtool.tests import UrlTest
from cdprocessing import views

class CdProcessingUrlTests(UrlTest):

    def test_single_url_resolves_to_single_run_page_view(self):
        self.check_url_returns_view("/single/", views.single_run)
