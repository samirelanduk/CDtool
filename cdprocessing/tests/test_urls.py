from cdtools.tests import UrlTest
from cdprocessing import views

class CdProcessingUrlTests(UrlTest):

    def test_home_page_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/", views.home_page)


    def test_home_page_url_resolves_to_home_page_view(self):
        self.check_url_returns_view("/single/", views.single_run)
