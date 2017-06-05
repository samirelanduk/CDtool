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

        # Thw window is resized to mobile proportions
        self.browser.set_window_size(350, 600)

        # The nav is no longer visible but there is a menu bar now
        self.assertFalse(nav.is_displayed())
        menu_icon = header.find_element_by_id("menu-icon")
        self.assertTrue(menu_icon.is_displayed())
        self.assertGreater(
         menu_icon.location["x"], header.size["width"] / 2
        )

        # Clicking it makes the menu appear
        menu_icon.click()
        self.assertTrue(nav.is_displayed())
        self.assertEqual(nav_links[0].location["y"], header.size["height"])
        self.assertGreater(nav_links[1].location["y"], nav_links[0].location["y"])
        menu_icon.click()
        sleep(1)
        self.assertFalse(nav.is_displayed())

        # Thw window is resized back and everything is back to how it was
        self.browser.set_window_size(800, 600)
        self.assertTrue(nav.is_displayed())
        self.assertFalse(menu_icon.is_displayed())



    def test_footer_layout(self):
        # The user goes to the main page
        self.get("/")

        # There is a footer at the bottom
        footer = self.browser.find_element_by_tag_name("footer")
        self.assertGreater(footer.location["y"], 500)

        # There are at least two lists of links, each having at least three
        lists = footer.find_elements_by_class_name("footer-list")
        self.assertGreaterEqual(len(lists), 2)
        for links in lists:
            self.assertGreaterEqual(len(links.find_elements_by_tag_name("a")), 3)

        # The lists are side by side
        self.assertGreater(lists[1].location["x"], lists[0].location["x"])

        # Thw window is resized to mobile proportions
        self.browser.set_window_size(350, 600)

        # Now the lists are on top of each other
        self.assertGreater(lists[1].location["y"], lists[0].location["y"])


class ChangelogTests(FunctionalTest):

    def test_changelog_structure(self):
        pass



class HelpTests(FunctionalTest):

    def test_help_structure(self):
        pass
