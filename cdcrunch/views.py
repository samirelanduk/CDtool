from django.shortcuts import render

# Create your views here.
def tool_page(request):
    if request.method == "POST":
        return render(request, "tool.html", {"output": True})
    return render(request, "tool.html")
