from time import sleep
from .base import FunctionalTest

class LayoutTests(FunctionalTest):

    def test_header_layout(self):
        # The user goes to the main page
        self.get("/")

        # There is a header with a logo to the left
        header = self.browser.find_element_by_tag_name("header")
        logo = header.find_element_by_id("logo")
        self.assertEqual(logo.text, "CDtool")
        self.assertLess(
         logo.location["x"] + logo.size["width"], header.size["width"] / 2
        )

        # The navigation menu is to the right
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("li")
        self.assertEqual(len(nav_links), 2)
        self.assertEqual(nav_links[0].text, "Help")
        self.assertEqual(nav_links[1].text, "About")
        self.assertEqual(
         nav.location["y"] + nav.size["height"],
         header.location["y"] + header.size["height"]
        )



    def test_footer_layout(self):
        pass



class ChangelogTests(FunctionalTest):

    def test_changelog_structure(self):
        pass



class HelpTests(FunctionalTest):

    def test_help_structure(self):
        pass
