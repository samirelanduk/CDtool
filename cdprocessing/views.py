from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    if request.method == "POST":
        return render(request, "single.html", {"display_chart": True, "contents": list(request.FILES["file"])})
    return render(request, "single.html", {"display_chart": False})
