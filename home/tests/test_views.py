from cdtool.tests import ViewTest

class ChangelogViewTests(ViewTest):

    def test_changelog_view_uses_changelog_template(self):
        response = self.client.get("/changelog/")
        self.assertTemplateUsed(response, "changelog.html")



class HelpViewTests(ViewTest):

    def test_help_view_uses_help_template(self):
        response = self.client.get("/help/")
        self.assertTemplateUsed(response, "help.html")
