from cdtool.tests import UrlTest
from home import views

class HomeUrlTests(UrlTest):

    def test_changelog_url_resolves_to_changelog_view(self):
        self.check_url_returns_view("/changelog/", views.changelog_page)
