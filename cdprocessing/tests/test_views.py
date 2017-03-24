from datetime import datetime
from cdtool.tests import ViewTest
from cdtool import version

class HomePageViewTests(ViewTest):

    def test_home_view_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")



class SingleRunViewGetTests(ViewTest):

    def test_single_run_view_uses_single_run_template(self):
        response = self.client.get("/single/")
        self.assertTemplateUsed(response, "single.html")


    def test_single_run_view_doesnt_normally_order_chart_to_display(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_chart"])



class SingleRunViewBlankPostTests(ViewTest):

    def test_post_blank_files_makes_single_run_view_display_single_run_template(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_chart_display_on_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertTrue(response.context["display_chart"])


    def test_correct_title_on_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["title"].lower())


    def test_correct_min_and_max_from_single_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 275)
        self.assertEqual(response.context["max"], 279)


    def test_correct_min_and_max_from_multi_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        self.assertEqual(response.context["min"], 275)
        self.assertEqual(response.context["max"], 279)


    def test_series_pull_from_single_scan_blank_file(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["series"], [
         [279.0, -0.006], [278.0, 0.044], [277.0, 0.031],
         [276.0, -0.158], [275.0, -0.151]
        ])


    def test_single_run_view_averages_multiple_blank_scans(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        self.assertAlmostEqual(
         response.context["series"][0][1],
         -0.0265, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][1][1],
         0.041, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][2][1],
         -0.1195, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][3][1],
         -0.021, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][4][1],
         -0.0015, delta=0.005
        )


    def test_series_puts_correct_filename_from_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["filename"].lower())



class SingleRunViewSamplePostTests(ViewTest):

    def test_post_sample_files_makes_single_run_view_display_single_run_template(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_chart_display_on_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertTrue(response.context["display_chart"])


    def test_correct_title_on_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["title"].lower())


    def test_correct_min_and_max_from_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 275)
        self.assertEqual(response.context["max"], 279)


    def test_correct_min_and_max_from_multi_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.multi_scan_file
        })
        self.assertEqual(response.context["min"], 275)
        self.assertEqual(response.context["max"], 279)


    def test_series_pull_from_single_scan_sample_file(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertEqual(response.context["series"], [
         [279.0, -0.006], [278.0, 0.044], [277.0, 0.031],
         [276.0, -0.158], [275.0, -0.151]
        ])


    def test_single_run_view_averages_multiple_sample_scans(self):
        response = self.client.post("/single/", data={
         "sample": self.multi_scan_file
        })
        self.assertAlmostEqual(
         response.context["series"][0][1],
         -0.0265, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][1][1],
         0.041, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][2][1],
         -0.1195, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][3][1],
         -0.021, delta=0.005
        )
        self.assertAlmostEqual(
         response.context["series"][4][1],
         -0.0015, delta=0.005
        )


    def test_series_puts_correct_filename_from_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["filename"].lower())



class SingleRunViewFileProductionTests(ViewTest):

    def test_single_run_view_sends_file_if_series_given(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertEqual(response["Content-Type"], "application/plain-text")


    def test_file_returned_uses_the_name_single_run_view_given(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertIn("test.dat", response["Content-Disposition"])


    def test_assert_file_produced_has_current_version(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertContains(response, version)


    def test_file_returned_uses_current_date(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertContains(response, datetime.now().strftime("%Y"))
        self.assertContains(response, datetime.now().strftime("%B"))
        self.assertContains(response, datetime.now().strftime("%A"))


    def test_file_returned_has_provided_series(self):
        response = self.client.post("/single/", data={
         "series": "[[280.0, 0.174], [279.0, 0.099], [278.0, 0.291]]",
         "filename": "test.dat"
        })
        lines = response.content.decode().split("\n")
        self.assertEqual(
         [float(value) for value in lines[-3].split()],
         [280, 0.174]
        )
        self.assertEqual(
         [float(value) for value in lines[-2].split()],
         [279, 0.099]
        )
        self.assertEqual(
         [float(value) for value in lines[-1].split()],
         [278, 0.291]
        )
