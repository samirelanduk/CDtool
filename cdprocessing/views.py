from django.shortcuts import render
from cdprocessing.functions import clean_file, extract_series, get_wavelengths

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    if request.method == "POST":
        lines = clean_file(list(request.FILES["file"]))
        series = extract_series(lines)
        wavelengths = get_wavelengths(series)
        return render(request, "single.html", {
         "display_chart": True,
         "min": min(wavelengths),
         "max": max(wavelengths)
        })
    return render(request, "single.html", {"display_chart": False})
