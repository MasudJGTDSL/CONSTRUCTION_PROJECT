from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "accounts/dashboard.html", {"data": "This is Data"})
