from datetime import datetime
import json
from inferi import Variable
from django.shortcuts import render
from django.http.response import HttpResponse
from cdtool import version
from cdcrunch import parse, files

series = {
 "name": "",
 "values": [],
 "errors": [],
 "color": "",
 "width": 0,
}

COLORS = ["#F2671F", "#C91B26", "#9C0F5F"] * 30

# Create your views here.
def tool_page(request):
    if request.method == "POST":
        if "series" in request.POST:
            return download_view(request)
        if "raw-files" not in request.FILES:
            return render(
             request, "tool.html", {"error_text": "You didn't submit any files."}
            )
        scans = []
        for f in request.FILES.getlist("raw-files"):
            scans += parse.extract_all_scans(f)
        if not scans:
            return render(request, "tool.html", {
             "error_text": "There were no scans found in the file(s) provided."
            })
        average = scans[0]
        if len(scans) > 1:
            average = [scans[0][0], Variable.average(*[scan[1] for scan in scans], sd_err=True)]
        average[1] = average[1].values(error=True)
        data = series.copy()
        data["name"] = request.POST.get("sample-name", "")
        data["color"], data["width"] = "#4A9586", 1.5
        data["raw"], data["baseline"] = {}, {}
        data["values"] = [[wav, val.value()] for wav, val in zip(*average)]
        data["errors"] = [
         [wav, *val.error_range()]
        for wav, val in zip(*average)]
        data["scans"] = []
        if len(scans) > 1:
            for index, scan in enumerate(scans):
                scan[1] = scan[1].values(error=True)
                d = series.copy()
                del d["name"]
                d["width"] = 1
                d["color"] = COLORS[index]
                d["values"] = [[wav, val.value()] for wav, val in zip(*scan)]
                d["errors"] = [[wav, *val.error_range()] for wav, val in zip(*scan)]
                data["scans"].append(d)
        file_series = [
         [wav, value.value(), value.error()] for wav, value in zip(*average)
        ][::-1]
        return render(request, "tool.html", {
         "output": True,
         "title": request.POST.get("exp-name", ""),
         "x_min": average[0].min(),
         "x_max": average[0].max(),
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

    title = title if title else "cdresults"
    return title.lower().replace(" ", "_").replace(":", "-").replace(
     "@", "-") + ".dat"
