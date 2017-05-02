import json
from datetime import datetime
from django.shortcuts import render
from django.http.response import HttpResponse
from cdprocessing import functions, file_templates
from cdtool import version

# Create your views here.
def single_run(request):
    """This is the view which handles all requests coming for the single run
    page at /single/. If it's a GET request it just returns the template for the
    page and doesn't do anything else other than telling it not to display the
    chart.

    If it's a POST request, the view examines the request to see where it should
    pass the request to. If the request contains a series, it sends the request
    to the view which generates the output files. If the request contains sample
    files, it sends the request to the view which processes data files."""

    if request.method == "POST":
        if "series" in request.POST:
            return file_producing_view(request)
        elif "sample_files" in request.FILES:
            return processing_view(request)
        else:
            return render(request, "single.html", {
             "display_chart": False,
             "error_text": "You must supply at least one file."
            })
    else:
        return render(request, "single.html", {"display_output": False})


def processing_view(request):
    """This is the view which takes in the data files and decides what needs to
    be done with them.

    It will get the scans from the sample files, and if there is only one file
    with only one scan in it, it will send the request to the single sample scan
    view, along with the scan it extracted."""

    input_files = request.FILES.getlist("sample_files")
    scans = functions.extract_all_series(input_files[0])
    if len(scans) > 1:
        return multi_sample_scan_view(request, scans)
    elif len(scans):
        return one_sample_scan_view(request, scans[0])
    else:
        return render(request, "single.html", {
         "display_chart": False,
         "error_text": "No scans were found in the file(s) given."
        })


def one_sample_scan_view(request, scan):
    """This is the view which processes requests which contain a single sample
    scan."""

    min_wavelength, max_wavelength = scan[-1][0], scan[0][0]
    return render(request, "single.html", {
     "display_output": True,
     "title": request.POST.get("title"),
     "min": min_wavelength,
     "max": max_wavelength,
     "main_series": [[wav, cd] for wav, cd, error in scan][::-1],
     "main_error": [[wav, cd - error, cd + error] for wav, cd, error in scan][::-1],
     "sample_name": request.POST.get("sample_name"),
     "file_series": scan,
     "file_name": functions.get_file_name(request.POST.get("title")) + ".dat"
    })


def multi_sample_scan_view(request, scans):
    """This is the view which processes requests which contain multiple sample
    scans."""

    average = functions.average_series(scans)
    min_wavelength, max_wavelength = min([w[0] for w in average]), max([w[0] for w in average])
    return render(request, "single.html", {
     "display_output": True,
     "title": request.POST.get("title"),
     "min": min_wavelength,
     "max": max_wavelength,
     "main_series": [[wav, cd] for wav, cd, error in average][::-1],
     "main_error": [[wav, cd - error, cd + error] for wav, cd, error in average][::-1],
    })


def file_producing_view(request):
    """This is the view that handles requests to produce a data file. This needs
    the data to go into the file to be already in the POST request as a JSON
    object.

    The data file will be returned as a downloadable file."""

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
