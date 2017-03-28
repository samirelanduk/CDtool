from datetime import datetime
from unittest.mock import patch, Mock
from django.http.response import HttpResponse
from cdtool.tests import ViewTest
from cdtool import version

class SingleRunViewTests(ViewTest):

    def test_single_run_view_uses_single_run_template(self):
        response = self.client.get("/single/")
        self.assertTemplateUsed(response, "single.html")


    def test_single_run_view_doesnt_normally_order_chart_to_display(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_chart"])


    @patch("cdprocessing.views.averaging_view")
    def test_single_run_view_uses_averaging_view_on_blank_posts(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIs(response, view_output)


    @patch("cdprocessing.views.averaging_view")
    def test_single_run_view_uses_averaging_view_on_sample_posts(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIs(response, view_output)


    @patch("cdprocessing.views.file_producing_view")
    def test_single_run_view_uses_file_production_view_on_series_posts(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "series": [[1, 2]]
        })
        self.assertIs(response, view_output)


    def test_single_run_view_returns_errors_if_no_files_given_in_post(self):
        response = self.client.post("/single/")
        self.assertIn("no file", response.context["error_text"].lower())



class AveragingViewTests(ViewTest):

    def test_averaging_view_uses_single_run_template(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_averaging_view_makes_chart_display_true(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertTrue(response.context["display_chart"])


    def test_averaging_view_gets_correct_title_on_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["title"].lower())


    def test_averaging_view_gets_correct_title_on_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["title"].lower())


    def test_averaging_view_sends_error_if_no_series(self):
        response = self.client.post("/single/", data={
         "blank": self.no_scan_file
        })
        self.assertIn("problem", response.context["error_text"].lower())


    def test_averaging_view_gets_correct_min_and_max_from_single_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 277)
        self.assertEqual(response.context["max"], 279)


    def test_averaging_view_gets_correct_min_and_max_from_multi_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        self.assertEqual(response.context["min"], 277)
        self.assertEqual(response.context["max"], 279)


    def test_averaging_view_gives_correct_absorbance_from_single_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["average_absorbance"], [
         [279.0, -0.006], [278.0, 0.044], [277.0, 0.031]
        ])


    def test_averaging_view_gives_correct_absorbance_from_multi_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        absorbance = response.context["average_absorbance"]
        self.assertEqual(len(absorbance), 3)
        self.assertEqual(len(absorbance[0]), 2)
        self.assertEqual(absorbance[0][0], 279)
        self.assertAlmostEqual(absorbance[0][1], -0.131, delta=0.005)
        self.assertEqual(len(absorbance[1]), 2)
        self.assertEqual(absorbance[1][0], 278)
        self.assertAlmostEqual(absorbance[1][1], 0.0307, delta=0.005)
        self.assertEqual(len(absorbance[2]), 2)
        self.assertEqual(absorbance[2][0], 277)
        self.assertAlmostEqual(absorbance[2][1], -0.1397, delta=0.005)


    def test_averaging_view_gives_correct_absorbance_from_multi_file_post(self):
        response = self.client.post("/single/", data={
         "blank": [self.multi_scan_file, self.single_scan_file]
        })
        absorbance = response.context["average_absorbance"]
        self.assertEqual(len(absorbance), 3)
        self.assertEqual(len(absorbance[0]), 2)
        self.assertEqual(absorbance[0][0], 279)
        self.assertAlmostEqual(absorbance[0][1], -0.09975, delta=0.005)
        self.assertEqual(len(absorbance[1]), 2)
        self.assertEqual(absorbance[1][0], 278)
        self.assertAlmostEqual(absorbance[1][1], 0.034, delta=0.005)
        self.assertEqual(len(absorbance[2]), 2)
        self.assertEqual(absorbance[2][0], 277)
        self.assertAlmostEqual(absorbance[2][1], -0.097, delta=0.005)


    def test_averaging_view_sends_no_errors_in_single_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["errors"], [])


    def test_averaging_view_gives_correct_errors_in_multi_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        errors = response.context["errors"]
        self.assertEqual(len(errors), 3)
        self.assertEqual(len(errors[0]), 3)
        self.assertEqual(errors[0][0], 279)
        self.assertAlmostEqual(errors[0][1], -0.236, delta=0.005)
        self.assertAlmostEqual(errors[0][2], -0.0258, delta=0.005)
        self.assertEqual(len(errors[1]), 3)
        self.assertEqual(errors[1][0], 278)
        self.assertAlmostEqual(errors[1][1], 0.0203, delta=0.005)
        self.assertAlmostEqual(errors[1][2], 0.041, delta=0.005)
        self.assertEqual(len(errors[2]), 3)
        self.assertEqual(errors[2][0], 277)
        self.assertAlmostEqual(errors[2][1], -0.2317, delta=0.005)
        self.assertAlmostEqual(errors[2][2], -0.048, delta=0.005)


    def test_averaging_view_gives_correct_errors_in_multi_file_post(self):
        response = self.client.post("/single/", data={
         "blank": [self.multi_scan_file, self.single_scan_file]
        })
        errors = response.context["errors"]
        self.assertEqual(len(errors), 3)
        self.assertEqual(len(errors[0]), 3)
        self.assertEqual(errors[0][0], 279)
        self.assertAlmostEqual(errors[0][1], -0.18, delta=0.005)
        self.assertAlmostEqual(errors[0][2], -0.019, delta=0.005)
        self.assertEqual(len(errors[1]), 3)
        self.assertEqual(errors[1][0], 278)
        self.assertAlmostEqual(errors[1][1], 0.02596, delta=0.005)
        self.assertAlmostEqual(errors[1][2], 0.042, delta=0.005)
        self.assertEqual(len(errors[2]), 3)
        self.assertEqual(errors[2][0], 277)
        self.assertAlmostEqual(errors[2][1], -0.1748, delta=0.005)
        self.assertAlmostEqual(errors[2][2], -0.0192, delta=0.005)


    def test_averaging_view_sends_no_input_series_for_single_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["input_series"], [])


    def test_averaging_view_sends_correct_input_series_for_multi_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        self.assertEqual(response.context["input_series"], [
         [[279, -0.006], [278, 0.042], [277, 0.036]],
         [[279, -0.047], [278, 0.040], [277, -0.275]],
         [[279, -0.34], [278, 0.01], [277, -0.18]],
        ])


    def test_averaging_view_sends_correct_input_series_for_multi_file_post(self):
        response = self.client.post("/single/", data={
         "blank": [self.multi_scan_file, self.single_scan_file]
        })
        self.assertEqual(response.context["input_series"], [
         [[279, -0.006], [278, 0.042], [277, 0.036]],
         [[279, -0.047], [278, 0.040], [277, -0.275]],
         [[279, -0.34], [278, 0.01], [277, -0.18]],
         [[279, -0.006], [278, 0.044], [277, 0.031]],
        ])


    def test_averaging_view_puts_correct_filename_from_blank_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertIn("blank", response.context["filename"].lower())


    def test_averaging_view_puts_correct_filename_from_sample_post(self):
        response = self.client.post("/single/", data={
         "sample": self.single_scan_file
        })
        self.assertIn("sample", response.context["filename"].lower())


    def test_averaging_view_gives_correct_file_series_from_single_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.single_scan_file
        })
        self.assertEqual(response.context["file_series"], [
         [279.0, -0.006, 0], [278.0, 0.044, 0], [277.0, 0.031, 0]
        ])


    def test_averaging_view_gives_correct_file_series_from_multi_scan_post(self):
        response = self.client.post("/single/", data={
         "blank": self.multi_scan_file
        })
        file_series = response.context["file_series"]
        self.assertEqual(len(file_series), 3)
        self.assertEqual(len(file_series[0]), 3)
        self.assertEqual(file_series[0][0], 279)
        self.assertAlmostEqual(file_series[0][1], -0.131, delta=0.005)
        self.assertAlmostEqual(file_series[0][2], 0.105, delta=0.005)
        self.assertEqual(len(file_series[1]), 3)
        self.assertEqual(file_series[1][0], 278)
        self.assertAlmostEqual(file_series[1][1], 0.0307, delta=0.005)
        self.assertAlmostEqual(file_series[1][2], 0.0103, delta=0.005)
        self.assertEqual(len(file_series[2]), 3)
        self.assertEqual(file_series[2][0], 277)
        self.assertAlmostEqual(file_series[2][1], -0.1397, delta=0.005)
        self.assertAlmostEqual(file_series[2][2], 0.092, delta=0.005)


    def test_averaging_view_gives_correct_file_series_from_multi_file_post(self):
        response = self.client.post("/single/", data={
         "blank": [self.multi_scan_file, self.single_scan_file]
        })
        file_series = response.context["file_series"]
        self.assertEqual(len(file_series), 3)
        self.assertEqual(len(file_series[0]), 3)
        self.assertEqual(file_series[0][0], 279)
        self.assertAlmostEqual(file_series[0][1], -0.09975, delta=0.005)
        self.assertAlmostEqual(file_series[0][2], 0.08066, delta=0.005)
        self.assertEqual(len(file_series[1]), 3)
        self.assertEqual(file_series[1][0], 278)
        self.assertAlmostEqual(file_series[1][1], 0.034, delta=0.005)
        self.assertAlmostEqual(file_series[1][2], 0.00804, delta=0.005)
        self.assertEqual(len(file_series[2]), 3)
        self.assertEqual(file_series[2][0], 277)
        self.assertAlmostEqual(file_series[2][1], -0.097, delta=0.005)
        self.assertAlmostEqual(file_series[2][2], 0.0778, delta=0.005)



class FileProducingViewTests(ViewTest):

    def test_file_producing_view_sends_file_if_series_given(self):
        response = self.client.post("/single/", data={
         "series": "[]",
         "filename": "test.dat"
        })
        self.assertEqual(response["Content-Type"], "application/plain-text")


    def test_file_producing_view_sends_file_returned_with_the_name_given(self):
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
         "series": "[[280.0, 0.17, 0.1], [279.0, 0.99, 0.2], [278.0, 0.2, 0.3]]",
         "filename": "test.dat"
        })
        lines = response.content.decode().split("\n")
        self.assertEqual(
         [float(value) for value in lines[-3].split()],
         [280, 0.17, 0.1]
        )
        self.assertEqual(
         [float(value) for value in lines[-2].split()],
         [279, 0.99, 0.2]
        )
        self.assertEqual(
         [float(value) for value in lines[-1].split()],
         [278, 0.2, 0.3]
        )




'''
class SingleRunViewFileProductionTests(ViewTest):


    '''
