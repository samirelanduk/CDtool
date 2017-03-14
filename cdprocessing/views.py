from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def single_run(request):
    return render(request, "single.html")
