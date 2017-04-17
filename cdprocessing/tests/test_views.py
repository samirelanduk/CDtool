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
    def test_processing_view_sends_single_scan(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        args, kwargs = mock_view.call_args
        scan = args[1]
        self.assertEqual(
         scan,
         [[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]]
        )


    @patch("cdprocessing.views.average_sample_view")
    def test_processing_view_uses_sample_averaging_view_if_multiple_sample_scan(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        self.assertIs(response, view_output)


    @patch("cdprocessing.views.average_sample_view")
    def test_processing_view_sends_all_scans(self, mock_view):
        view_output = HttpResponse()
        mock_view.return_value = view_output
        response = self.client.post("/single/", data={
         "sample_files": self.multi_scan_file
        })
        args, kwargs = mock_view.call_args
        scan = args[1]
        self.assertEqual(
         scan,
         [[[279, 1.0, 0.5], [278, -4.0, 0.4], [277, 12.0, 0.3]],
          [[279, 0.0, 0.2], [278, -5.0, 0.75], [277, 11.0, 0.4]],
          [[279, 2.0, 0.1], [278, -3.0, 0.3], [277, 13.0, 0.2]]]
        )



class OneSampleScanViewTests(ViewTest):

    def test_single_sample_scan_view_uses_single_run_template(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertTemplateUsed(response, "single.html")


    def test_single_sample_scan_view_makes_chart_display_true(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file,
        })
        self.assertTrue(response.context["display_chart"])


    def test_single_sample_scan_view_gets_correct_title(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file,
         "title": "Some title"
        })
        self.assertEqual("Some title", response.context["title"])


    def test_single_sample_scan_view_gets_correct_min_and_max(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["min"], 277)
        self.assertEqual(response.context["max"], 279)


    def test_single_sample_scan_view_gives_correct_main_series(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["main_series"], [
         [279.0, 1], [278.0, -4], [277.0, 12]
        ])


    def test_single_sample_gives_correct_main_error(self):
        response = self.client.post("/single/", data={
         "sample_files": self.single_scan_file
        })
        self.assertEqual(response.context["main_error"], [
         [279.0, 0.5, 1.5], [278.0, -4.4, -3.6], [277.0, 11.7, 12.3]
        ])


    def test_single_sample_view_gets_correct_sample_name(self):
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
