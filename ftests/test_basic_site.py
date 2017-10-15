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
        # The user goes to the main page
        self.get("/")

        # The footer has a section for useful links, with a changelog link
        footer = self.browser.find_element_by_tag_name("footer")
        useful_links = footer.find_elements_by_class_name("footer-list")[0]
        useful_links = useful_links.find_elements_by_tag_name("a")
        changelog_link = [a for a in useful_links if "changelog" in a.text.lower()][0]

        # They click the changelog link and go to the changelog page
        self.scroll_to(changelog_link)
        changelog_link.click()
        self.check_page("/changelog/")

        # The changlog is there
        heading = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(heading.text, "Changelog")
        releases = self.browser.find_elements_by_class_name("release")
        self.assertTrue(releases)
        for release in releases:
            release_title = release.find_element_by_tag_name("h2")
            self.assertEqual(release_title.text.count("."), 2)
            release_date = release.find_element_by_class_name("release-date")
            self.assertGreater(len(release.find_elements_by_tag_name("li")), 0)

        # None of the h2 links are the same
        h2s = self.browser.find_elements_by_tag_name("h2")
        h2_links = [h2.find_element_by_tag_name("a").get_attribute("href") for h2 in h2s]
        self.assertEqual(len(h2_links), len(set(h2_links)))

        # They click the main logo to go back to the home page
        header = self.browser.find_element_by_tag_name("header")
        logo = header.find_element_by_id("logo")
        logo.click()
        self.check_page("/")



class HelpTests(FunctionalTest):

    def test_help_structure(self):
        # The user goes to the main page
        self.get("/")

        # There is a link to the help page in the header, which they follow
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[0].click()
        self.check_page("/help/")

        # There is a heading, and numerous sub-headings
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertIn("help", h1.text.lower())
        h2s = self.browser.find_elements_by_tag_name("h2")
        self.assertGreater(len(h2s), 2)

        # They click the main logo to go back to the home page
        header = self.browser.find_element_by_tag_name("header")
        logo = header.find_element_by_id("logo")
        logo.click()
        self.check_page("/")



class AboutTests(FunctionalTest):

    def test_help_structure(self):
        # The user goes to the main page
        self.get("/")

        # There is a link to the about page in the header, which they follow
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        nav_links[1].click()
        self.check_page("/about/")

        # There is a heading
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertIn("about", h1.text.lower())

        # They click the main logo to go back to the home page
        header = self.browser.find_element_by_tag_name("header")
        logo = header.find_element_by_id("logo")
        logo.click()
        self.check_page("/")
