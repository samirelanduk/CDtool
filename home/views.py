from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, "home.html")


def changelog_page(request):
    return render(request, "changelog.html")
