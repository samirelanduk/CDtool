from datetime import datetime
from django.shortcuts import render
from django.http.response import HttpResponse
from cdcrunch import parse, downloads

def tool_page(request):
    """The first port of call for requests to the ``/`` URL. It forwards the
    request to the relevant view based on whether the request is ``GET`` or
    ``POST``"""

    if request.method == "POST":
        return root_post(request)
    else:
        return root_get(request)


def root_get(request):
    """If the root page is requested with a ``GET`` request, the basic tool
    page is returned and nothing more."""

    return render(request, "tool.html")


def root_post(request):
    """If the root page is requested with a ``POST`` request, CDtool checks to
    see if a series is submitted with it. If so, the request is sent to the
    download view. Otherwise, the parse view is used."""

    if "series" in request.POST:
        return root_download(request)
    else:
        return root_parse(request)


def root_parse(request):
    """This is the view that provides a response if the user submits scan files.
    It extracts the data contained in them, combines them as necessary, and
    returns the relevant response."""

    if not request.FILES.getlist("raw-files"):
        if request.FILES.getlist("baseline-files"):
            return render(request, "tool.html", {
             "error_text": "There were no raw files to subtract baseline from."
            })
        return render(request, "tool.html", {
         "error_text": "You didn't submit any files."
        })
    sample = parse.files_to_sample(
     request.FILES.getlist("raw-files"),
     request.FILES.getlist("baseline-files"),
     name=request.POST["sample-name"]
    )

    if sample is None:
        return render(request, "tool.html", {
         "error_text": "There were no scans found in the file(s) provided."
        })
    return render(request, "tool.html", {
     "output": True, "title": request.POST["exp-name"], "sample": sample
    })


def root_download(request):
    """This is the view that sends a file containing the main series when a
    series object is posted to it."""

    filebody = downloads.series_to_file(request.POST["series"])
    response = HttpResponse(
     filebody, content_type="application/plain-text"
    )
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
     downloads.produce_filename(request.POST["name"])
    )
    return response
