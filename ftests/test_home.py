from time import sleep
from .base import FunctionalTest

class ChangelogTests(FunctionalTest):

    def test_can_read_changelog(self):
        # User goes to the home page
        self.browser.get(self.live_server_url + "/")

        # The footer has a section for useful links, with a changelog link
        footer = self.browser.find_element_by_tag_name("footer")
        useful_links = footer.find_elements_by_class_name("footer-list")[0]
        useful_links = useful_links.find_elements_by_tag_name("a")
        changelog_link = [a for a in useful_links if "changelog" in a.text.lower()][0]

        # They click it and go to the changelog
        changelog_link.click()
        sleep(1)
        self.assertEqual(
         self.browser.current_url,
         self.live_server_url + "/changelog/"
        )

        # There are a bunch of releases
        releases = self.browser.find_elements_by_class_name("release")
        self.assertGreater(len(releases), 0)

        # Every release has a heading, a date, and unordered list
        for release in releases:
            heading = release.find_element_by_tag_name("h2")
            date = release.find_element_by_id("release-date")
            ul = release.find_element_by_tag_name("ul")
