from datetime import datetime
from unittest.mock import patch, Mock
from django.http.response import HttpResponse
from cdtool.tests import ViewTest
from cdtool import version

class SingleRunViewTests(ViewTest):

    def test_single_run_view_uses_single_run_template(self):
        response = self.client.get("/single/")
        self.assertTemplateUsed(response, "single.html")


    def test_single_run_view_doesnt_normally_order_output_to_display(self):
        response = self.client.get("/single/")
        self.assertFalse(response.context["display_output"])


    @patch("cdprocessing.views.processing_view")
    def test_single_run_view_uses_processing_view_on_sample_posts(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
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



class ProcessingViewTests(ViewTest):

    @patch("cdprocessing.views.one_sample_scan_view")
    def test_processing_view_uses_single_scan_view_if_one_sample_scan(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertIs(response, view_output)


    @patch("cdprocessing.views.one_sample_scan_view")
    @patch("cdprocessing.functions.extract_all_series")
    def test_processing_view_sends_single_scan(self, mock_extract, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        mock_extract.return_value = [
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        ]
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        args, kwargs = mock_view.call_args
        scan = args[1]
        self.assertEqual(
         scan,
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        )



class OneSampleScanViewTests(ViewTest):

    def test_single_sample_scan_view_uses_single_run_template(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_single_sample_scan_view_makes_output_display_true(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file,
        })
        self.assertTrue(response.context["display_output"])


    def test_single_sample_scan_view_gets_correct_title(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file,
         "title": "Some title"
        })
        self.assertEqual("Some title", response.context["title"])


    @patch("cdprocessing.functions.extract_all_series")
    def test_single_sample_scan_view_gets_correct_min_and_max(self, mock_extract):
        mock_extract.return_value = [
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        ]
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 277)
        self.assertEqual(response.context["max"], 279)


    @patch("cdprocessing.functions.extract_all_series")
    def test_single_sample_scan_view_gives_correct_main_series(self, mock_extract):
        mock_extract.return_value = [
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        ]
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["main_series"], [
         [279.0, 1], [278.0, -4], [277.0, 12]
        ])


    @patch("cdprocessing.functions.extract_all_series")
    def test_single_sample_gives_correct_main_error(self, mock_extract):
        mock_extract.return_value = [
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        ]
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["main_error"], [
         [279.0, 0.5, 1.5], [278.0, -4.4, -3.6], [277.0, 11.7, 12.3]
        ])


    '''def test_single_sample_view_gets_correct_sample_name(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file,
         "sample_name": "Some sample"
        })
        self.assertEqual("Some sample", response.context["sample_name"])


    def test_single_sample_view_view_gives_correct_file_series(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["file_series"], [
         [279.0, 1, 0.5], [278.0, -4, 0.4], [277.0, 12, 0.3]
        ])



class AverageSampleViewTests(ViewTest):

    def test_average_sample_view_uses_single_run_template(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_average_sample_view_makes_chart_display_true(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file,
        })
        self.assertTrue(response.context["display_chart"])


    def test_average_sample_view_gets_correct_title(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file,
         "title": "Some title"
        })
        self.assertEqual("Some title", response.context["title"])


    def test_average_sample_view_gets_correct_min_and_max(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertEqual(response.context["min"], 277)
        self.assertEqual(response.context["max"], 279)


    def test_average_sample_view_gives_correct_main_series(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertEqual(response.context["main_series"], [
         [279.0, 0], [278.0, -5], [277.0, 11]
        ])


    def test_average_sample_view_gives_correct_main_error(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        main_error = response.context["main_error"]
        self.assertEqual(len(main_error), 3)
        self.assertEqual(len(main_error[0]), 3)
        self.assertEqual(main_error[0][0], 279)
        self.assertAlmostEqual(main_error[0][1], -0.8165, delta=0.005)
        self.assertAlmostEqual(main_error[0][2], 0.8165, delta=0.005)
        self.assertEqual(len(main_error[1]), 3)
        self.assertEqual(main_error[1][0], 278)
        self.assertAlmostEqual(main_error[1][1], -5.8165, delta=0.005)
        self.assertAlmostEqual(main_error[1][2], -4.1835, delta=0.005)
        self.assertEqual(len(main_error[2]), 3)
        self.assertEqual(main_error[2][0], 277)
        self.assertAlmostEqual(main_error[2][1], 10.1835, delta=0.005)
        self.assertAlmostEqual(main_error[2][2], 11.8165, delta=0.005)


    def test_average_sample_view_gets_correct_sample_name(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file,
         "sample_name": "Some sample"
        })
        self.assertEqual("Some sample", response.context["sample_name"])


    def test_average_sample_view_sends_sample_scans(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertEqual(
         response.context["sample_scans"],
         [
          [[279.0, 1], [278.0, -4], [277.0, 12]],
          [[279.0, 0], [278.0, -5], [277.0, 11]],
          [[279.0, -1], [278.0, -6], [277.0, 10]],
         ]
        )


    def test_average_sample_view_gives_correct_file_series(self):
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertEqual(response.context["file_series"], [
         [279.0, 0, 0.816496580927726],
         [278.0, -5, 0.816496580927726],
         [277.0, 11, 0.816496580927726]
        ])



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
        )'''
