from django.shortcuts import render
from cdprocessing.functions import clean_file, extract_series

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    if request.method == "POST":
        lines = clean_file(list(request.FILES["file"]))
        series = extract_series(lines)
        return render(request, "single.html", {"display_chart": True, "contents": series})
    return render(request, "single.html", {"display_chart": False})
