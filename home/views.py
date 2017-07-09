from django.shortcuts import render

# Create your views here.
def changelog_page(request):
    return render(request, "changelog.html")
