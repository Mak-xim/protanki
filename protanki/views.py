from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "protanki/index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "../templates/information/about.html")

def tanks_info(request: HttpRequest) -> HttpResponse:
    return render(request, "../templates/information/tanks_info.html")
