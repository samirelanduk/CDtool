from datetime import datetime
import json
from django.shortcuts import render
from django.http.response import HttpResponse
from cdtool import version
from cdcrunch import parse, files

series = {
 "name": "",
 "values": [],
 "error": [],
 "color": "",
 "width": 0,
}

# Create your views here.
def tool_page(request):
    if request.method == "POST":
        if "series" in request.POST:
            return download_view(request)
        if "raw-files" not in request.FILES:
            return render(
             request, "tool.html", {"error_text": "You didn't submit any files."}
            )
        scans = parse.extract_all_scans(request.FILES.getlist("raw-files")[0])
        scan = scans[0]
        data = series.copy()
        data["name"] = request.POST.get("sample-name", "")
        data["color"], data["width"] = "#4A9586", 1.5
        data["raw"], data["baseline"] = {}, {}
        data["values"] = [[wav.value(), val.value()] for wav, val in zip(*scan)]
        data["errors"] = [
         [wav.value(), *val.error_range()]
        for wav, val in zip(*scan)]
        file_series = [
         [wav.value(), value.value(), value.error()] for wav, value in zip(*scan)
        ][::-1]
        return render(request, "tool.html", {
         "output": True,
         "title": request.POST.get("exp-name", ""),
         "x_min": scan[0].min(),
         "x_max": scan[0].max(),
         "data": [data],
         "file_series": file_series
        })
    return render(request, "tool.html")


def download_view(request):
    """Handles requests for data files"""

    header = files.data_file % (
     version,
     datetime.now().strftime("%d %B, %Y (%A)"),
     datetime.now().strftime("%H:%M:%S (UK Time)")
    )
    series = json.loads(request.POST["series"])
    lines = ["{:.1f}         {:10.4f}   {:10.4f}".format(
     line[0],
     line[1],
     line[2]
    ) for line in series]
    response = HttpResponse(
     header + "\n".join(lines), content_type="application/plain-text"
    )
    response["Content-Disposition"] = 'attachment; filename="%s"' % (
     produce_filename(request.POST["name"])
    )
    return response


def produce_filename(title):
    """Takes an experiment title and returns a valid filename."""

    return title.lower().replace(" ", "_").replace(":", "-").replace(
     "@", "-") + ".dat"
