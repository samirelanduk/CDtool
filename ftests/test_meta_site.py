from .base import FunctionalTest
from time import sleep

class HomePageTests(FunctionalTest):

    def test_home_page_general_structure(self):
        # The user goes to the home page
        self.browser.get(self.live_server_url)

        # There are four main sections to the body
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )

        # The footer has three



class HelpTests(FunctionalTest):

    def test_help_page_general_structure(self):
        pass
