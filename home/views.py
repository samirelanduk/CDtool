from django.shortcuts import render

# Create your views here.
def changelog_page(request):
    return render(request, "changelog.html")


def help_page(request):
    return render(request, "help.html")


def about_page(request):
    return render(request, "about.html")
