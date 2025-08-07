
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from users.forms import UserRegisterForm
from .models import FavoriteGun
from  .models import FavoriteBody
from .models import Gun, Body
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def index(request: HttpRequest) -> HttpResponse:
    form = UserRegisterForm()
    return render(request, "protanki/index.html", {'form': form})


def about(request: HttpRequest) -> HttpResponse:
    form = UserRegisterForm()
    return render(request, "../templates/information/about.html", {'form': form})

# @require_POST
@login_required
def add_favorite_gun(request, gun_id):
    FavoriteGun.objects.get_or_create(user=request.user, gun_id=gun_id)
    return JsonResponse({"status": "ok"})

@require_POST
@login_required
def remove_favorite_gun(request, gun_id):
    FavoriteGun.objects.filter(user=request.user, gun_id=gun_id).delete()
    return JsonResponse({"status": "ok"})

@require_POST
@login_required
def add_favorite_body(request, body_id):
    FavoriteBody.objects.get_or_create(user=request.user, body_id=body_id)
    return JsonResponse({"status": "ok"})

@require_POST
@login_required
def remove_favorite_body(request, body_id):
    FavoriteBody.objects.filter(user=request.user, body_id=body_id).delete()
    return JsonResponse({"status": "ok"})


@login_required
def favorites_view(request):
    favorite_guns = FavoriteGun.objects.filter(user=request.user).select_related('gun')
    favorite_bodies = FavoriteBody.objects.filter(user=request.user).select_related('body')

    return render(request, 'information/favorites.html', {
        'favorite_guns': favorite_guns,
        'favorite_bodies': favorite_bodies,
    })

def tanks_info(request: HttpRequest) -> HttpResponse:
    guns = Gun.objects.all()
    bodies = Body.objects.all()
    form = UserRegisterForm()


    guns_by_level = {
        'M0': [],
        'M1': [],
        'M2': [],
        'M3': [],
    }
    bodies_by_level = {
        'M0': [],
        'M1': [],
        'M2': [],
        'M3': [],
    }

    if request.user.is_authenticated and hasattr(request.user, 'favorite_guns_rel'):
        favorite_guns = set(request.user.favorite_guns_rel.values_list('gun_id', flat=True))
    else:
        favorite_guns = set()

    if request.user.is_authenticated and hasattr(request.user, 'favorite_bodies_rel'):
        favorite_bodies = set(request.user.favorite_bodies_rel.values_list('body_id', flat=True))
    else:
        favorite_bodies = set()

    context = {
        'guns': guns,
        'bodies': bodies,
        'guns_by_level': guns_by_level,
        'bodies_by_level': bodies_by_level,
        'favorite_guns': favorite_guns,
        'favorite_bodies': favorite_bodies,
    }

    for gun in guns:
        gun.damage_percent = min(int(gun.damage / 68 * 100), 100)
        gun.dpm_percent = min(int(gun.damage_minute / 187 * 100), 100)
        gun.recharge_percent = min(int(gun.recharge / 15 * 100), 100)
        gun.range_percent = min(int(gun.range / 150 * 100), 100)
        gun.power_percent = min(int(gun.power / 369 * 100), 100)

        guns_by_level.get(gun.level, []).append(gun)

    for body in bodies:
        body.armor_percent = min(int(body.armor / 1000 * 100), 100)
        body.max_speed_percent = min(int(body.max_speed / 10000 * 100), 100)
        body.turning_speed_percent = min(int(body.turning_speed / 10 * 100), 100)
        body.weight_percent = min(int(body.weight / 1000 * 100), 100)
        body.power_percent = min(int(body.power / 100 * 100), 100)

        bodies_by_level.get(body.level, []).append(body)



    return render(request, "information/tanks_info.html", {
        "context": context,
        'form': form,
        'guns': guns,
        'bodies': bodies,
        'guns_by_level': guns_by_level,
        'bodies_by_level': bodies_by_level,
        'favorite_guns': favorite_guns,
        'favorite_bodies': favorite_bodies,})
