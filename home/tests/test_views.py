from datetime import datetime
from cdtool.tests import ViewTest
from cdtool import version

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")



class ChangelogPageViewTests(ViewTest):

    def test_changelog_view_uses_changelog_template(self):
        response = self.client.get("/changelog/")
        self.assertTemplateUsed(response, "changelog.html")
