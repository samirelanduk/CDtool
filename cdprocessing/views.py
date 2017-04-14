import json
from datetime import datetime
from django.shortcuts import render
from django.http.response import HttpResponse
from cdprocessing import functions, file_templates
from cdtool import version

# Create your views here.
def single_run(request):
    if request.method == "POST":
        if "series" in request.POST:
            return file_producing_view(request)
        elif "sample_files" in request.FILES:
            return averaging_view(request)
        else:
            return render(request, "single.html", {
             "display_chart": False, "error_text": "No files were supplied."
            })
    else:
        return render(request, "single.html", {"display_chart": False})


def averaging_view(request):
    input_files = request.FILES.getlist("sample_files")
    scans = functions.extract_all_series(input_files[0])
    average_series = functions.average_series(scans)
    min_wavelength, max_wavelength = average_series[-1][0], average_series[0][0]
    main_series = [line[:2] for line in average_series]
    main_error = [[line[0], line[1] - line[2], line[1] + line[2]] for line in average_series]
    return render(request, "single.html", {
     "display_chart": True,
     "title": request.POST.get("title"),
     "min": min_wavelength,
     "max": max_wavelength,
     "main_series": main_series,
     "main_error": main_error,
     "sample_name": request.POST.get("sample_name"),
     "file_series": average_series
    })
    '''input_files = request.FILES.getlist("sample")
    all_series = []
    for input_file in input_files:
        try:
            all_series += functions.extract_all_series(input_file)
        except:
            return render(request, "single.html", {
             "display_chart": False, "error_text": "Problem parsing %s." % input_file
            })
    average_series = functions.average_series(all_series)

    average_absorbance = [line[:2] for line in average_series]
    errors = [[line[0]] + line[-2:] for line in average_series]
    if len(all_series) == 1: errors = []
    filename = "average_sample.dat" if request.FILES.get("sample")\
     else "average_blank.dat"
    file_series = [line[:3] for line in average_series]

    return render(request, "single.html", {
     "display_chart": True,
     "title": title,

     "average_absorbance": average_absorbance,
     "errors": errors,
     "input_series": all_series if len(all_series) > 1 else [],
     "filename": filename,
     "file_series": file_series
    })'''


def file_producing_view(request):
    header = file_templates.data_file % (
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
     request.POST["filename"]
    )
    return response
