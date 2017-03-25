import json
from datetime import datetime
from django.shortcuts import render
from django.http.response import HttpResponse
from cdprocessing import functions, file_templates
from cdtool import version

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    if request.method == "POST":
        if "series" in request.POST:
            series = json.loads(request.POST["series"])
            lines = ["{}   {}".format(line[0], line[1]) for line in series]
            header = file_templates.data_file % (
             version,
             datetime.now().strftime("%d %B, %Y (%A)"),
             datetime.now().strftime("%H:%M:%S (UK Time)")
            )
            response = HttpResponse(header + "\n".join(lines), content_type='application/plain-text')
            response['Content-Disposition'] = 'attachment; filename="%s"' % request.POST["filename"]
            return response
        else:
            lines, title, filename = None, None, None
            if request.FILES.get("blank"):
                lines = functions.clean_file(list(request.FILES["blank"]))
                title = "Blank"
                filename = "average_blank.dat"
            elif request.FILES.get("sample"):
                lines = functions.clean_file(list(request.FILES["sample"]))
                title = "Sample"
                filename = "average_sample.dat"
            float_groups = functions.get_float_groups(lines)
            big_series = functions.float_groups_to_big_series(float_groups)
            additional_series = functions.float_groups_to_extra_series(
             float_groups, big_series
            )
            series = [big_series] + additional_series
            wavelengths = functions.extract_wavelengths(big_series)
            raw_absorbances = functions.extract_absorbances(series)
            absorbances = [a[:2] for a in raw_absorbances]
            errors = [
             [a[0], a[1] - a[2], a[1] + a[2]]
            for a in raw_absorbances] if len(series) > 1 else []
            input_series = [functions.extract_absorbances([original_series]) for original_series in series]
            for i in input_series:
                [point.pop() for point in i]
            input_series = input_series[1:] + [input_series[0]]
            if len(series) == 1: input_series = []
            return render(request, "single.html", {
             "display_chart": True,
             "title": title,
             "min": min(wavelengths),
             "max": max(wavelengths),
             "series": absorbances,
             "errors": errors,
             "input_series": input_series,
             "filename": filename
            })
    return render(request, "single.html", {"display_chart": False})
