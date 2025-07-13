from django.shortcuts import render


def index(request):
    return render(request, "protanki/index.html")


def about(request):
    return render(request, "../templates/information/about.html")
