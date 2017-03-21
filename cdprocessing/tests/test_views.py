from cdtool.tests import ViewTest

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")



class SingleRunPageViewTests(ViewTest):

    def test_single_run_view_uses_single_run_template(self):
        response = self.client.get("/single/")
        self.assertTemplateUsed(response, "single.html")


    def test_chart_display_on_blank_post(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_chart"])
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertTrue(response.context["display_chart"])


    def test_chart_display_on_sample_post(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_chart"])
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertTrue(response.context["display_chart"])


    def test_single_run_view_can_select_blank_title(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["title"].lower())
        self.assertTrue(response.context["display_chart"])


    def test_single_run_view_can_select_blank_file_name(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["filename"].lower())


    def test_single_run_view_can_select_sample_title(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["title"].lower())


    def test_single_run_view_can_select_sample_file_name(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["filename"].lower())


    def test_single_run_view_can_pull_min_and_max_wavelength_from_single_scan(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 275)
        self.assertEqual(response.context["max"], 279)


    def test_single_run_view_can_pull_out_absorbance_from_single_scan(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["series"], [
         [279.0, -0.006],
         [278.0, 0.044],
         [277.0, 0.031],
         [276.0, -0.158],
         [275.0, -0.151],
        ])


    def test_single_run_view_returns_file_if_series_given(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertEqual(response["Content-Type"], "application/plain-text")
