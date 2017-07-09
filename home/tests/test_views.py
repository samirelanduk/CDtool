from cdtool.tests import ViewTest

class ChangelogViewTests(ViewTest):

    def test_changelog_view_uses_changelog_template(self):
        response = self.client.get("/changelog/")
        self.assertTemplateUsed(response, "changelog.html")
