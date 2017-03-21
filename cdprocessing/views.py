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
            response['Content-Disposition'] = 'attachment; filename="average_blank.dat"'
            return response
        lines = functions.clean_file(list(request.FILES["blank"]))
        float_groups = functions.get_float_groups(lines)
        series = functions.float_groups_to_series(float_groups)
        wavelengths = functions.extract_wavelengths(series)
        absorbances = functions.extract_absorbances(series)
        return render(request, "single.html", {
         "display_chart": True,
         "min": min(wavelengths),
         "max": max(wavelengths),
         "series": absorbances
        })
    return render(request, "single.html", {"display_chart": False})
