from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Gun, Body


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "protanki/index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "../templates/information/about.html")


def tanks_info(request: HttpRequest) -> HttpResponse:
    guns = Gun.objects.all()
    bodies = Body.objects.all()

    for gun in guns:
        gun.damage_percent = min(int(gun.damage / 68 * 100), 100)
        gun.dpm_percent = min(int(gun.damage_minute / 187 * 100), 100)
        gun.recharge_percent = min(int(gun.recharge / 15 * 100), 100)
        gun.range_percent = min(int(gun.range / 150 * 100), 100)
        gun.power_percent = min(int(gun.power / 369 * 100), 100)

    for body in bodies:
        body.armor_percent = min(int(body.armor / 1000 * 100), 100)
        body.max_speed_percent = min(int(body.max_speed / 10000 * 100), 100)
        body.turning_speed_percent = min(int(body.turning_speed / 10 * 100), 100)
        body.weight_percent = min(int(body.weight / 1000 * 100), 100)
        body.power_percent = min(int(body.power / 100 * 100), 100)



    return render(request, "information/tanks_info.html", {"guns": guns, "bodies": bodies})

