from django.shortcuts import render
from cdprocessing import functions

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    if request.method == "POST":
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
