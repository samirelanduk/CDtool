from django.shortcuts import render

# Create your views here.
def tool_page(request):
    return render(request, "tool.html")
