from django.shortcuts import render
from cdcrunch import parse

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
        scans = parse.extract_all_scans(request.FILES.getlist("raw-files")[0])
        scan = scans[0]
        data = series.copy()
        data["name"] = request.POST.get("sample-name", "")
        data["color"], data["width"] = "#4A9586", 1.5
        data["raw"], data["baseline"] = {}, {}
        data["values"] = [[wav.value(), val.value()] for wav, val in zip(*scan)]
        data["errors"] = [
         [wav.value(), val.value() - val.error(), val.value() + val.error()]
        for wav, val in zip(*scan)]
        return render(request, "tool.html", {
         "output": True,
         "title": request.POST.get("exp-name", ""),
         "x_min": scan[0].min(),
         "x_max": scan[0].max(),
         "data": [data]
        })
    return render(request, "tool.html")
