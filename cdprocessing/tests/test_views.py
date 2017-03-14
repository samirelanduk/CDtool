from cdtools.tests import ViewTest

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")



class SingleRunPageViewTests(ViewTest):

    def test_single_run_view_uses_single_run_template(self):
        response = self.client.get("/single/")
        self.assertTemplateUsed(response, "single.html")


    def test_chart_display_on_post(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_chart"])
        response = self.client.post("/single/")
        self.assertTrue(response.context["display_chart"])
