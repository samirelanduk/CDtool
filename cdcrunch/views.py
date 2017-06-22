from django.shortcuts import render
from cdcrunch import parse

# Create your views here.
def tool_page(request):
    if request.method == "POST":
        scans = parse.extract_all_scans(request.FILES.getlist("raw-files")[0])
        scan = scans[0]
        return render(request, "tool.html", {
         "output": True,
         "title": request.POST.get("exp-name", ""),
         "x_min": scan[0].min(),
         "x_max": scan[0].max()
        })
    return render(request, "tool.html")
