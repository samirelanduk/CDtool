from cdtool.tests import UrlTest
from home import views

class HomeUrlTests(UrlTest):

    def test_changelog_url_resolves_to_changelog_view(self):
        self.check_url_returns_view("/changelog/", views.changelog_page)


    def test_help_url_resolves_to_help_view(self):
        self.check_url_returns_view("/help/", views.help_page)


    def test_about_url_resolves_to_about_view(self):
        self.check_url_returns_view("/about/", views.about_page)
