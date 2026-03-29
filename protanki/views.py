from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Body, BodyComment, FavoriteBody, FavoriteGun, Gun, GunComment
from .utils import calculate_body_percentages, calculate_gun_percentages


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "protanki/index.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "../templates/information/about.html")


@login_required
def add_favorite_gun(request: HttpRequest, gun_id: int) -> JsonResponse:
    FavoriteGun.objects.get_or_create(user=request.user, gun_id=gun_id)
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def remove_favorite_gun(request: HttpRequest, gun_id: int) -> JsonResponse:
    FavoriteGun.objects.filter(user=request.user, gun_id=gun_id).delete()
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def add_favorite_body(request: HttpRequest, body_id: int) -> JsonResponse:
    FavoriteBody.objects.get_or_create(user=request.user, body_id=body_id)
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def remove_favorite_body(request: HttpRequest, body_id: int) -> JsonResponse:
    FavoriteBody.objects.filter(user=request.user, body_id=body_id).delete()
    return JsonResponse({"status": "ok"})


@login_required
def favorites_view(request: HttpRequest) -> HttpResponse:
    search_query = request.GET.get("q", "").strip().lower()

    favorite_guns_qs = FavoriteGun.objects.filter(user=request.user).select_related(
        "gun"
    )
    favorite_bodies_qs = FavoriteBody.objects.filter(user=request.user).select_related(
        "body"
    )

    favorite_guns = [fav.gun for fav in favorite_guns_qs]
    favorite_bodies = [fav.body for fav in favorite_bodies_qs]

    if search_query:
        favorite_guns = [
            gun
            for gun in favorite_guns
            if search_query in gun.name.lower()
            or search_query in gun.information.lower()
        ]
        favorite_bodies = [
            body
            for body in favorite_bodies
            if search_query in body.name.lower()
            or search_query in body.information.lower()
        ]

    # ✅ применяем утилиты
    favorite_guns = calculate_gun_percentages(favorite_guns)
    favorite_bodies = calculate_body_percentages(favorite_bodies)

    context = {
        "favorite_guns": favorite_guns,
        "favorite_bodies": favorite_bodies,
    }
    return render(request, "information/favorites.html", context)


def tanks_info(request: HttpRequest) -> HttpResponse:
    guns = Gun.objects.all().order_by("name")
    bodies = Body.objects.all().order_by("name")

    guns_by_level = {"M0": [], "M1": [], "M2": [], "M3": []}
    bodies_by_level = {"M0": [], "M1": [], "M2": [], "M3": []}

    if request.user.is_authenticated and hasattr(request.user, "favorite_guns_rel"):
        favorite_guns = set(
            request.user.favorite_guns_rel.values_list("gun_id", flat=True)
        )
    else:
        favorite_guns = set()

    if request.user.is_authenticated and hasattr(request.user, "favorite_bodies_rel"):
        favorite_bodies = set(
            request.user.favorite_bodies_rel.values_list("body_id", flat=True)
        )
    else:
        favorite_bodies = set()

    # ✅ применяем утилиты
    guns = calculate_gun_percentages(list(guns))
    bodies = calculate_body_percentages(list(bodies))

    for gun in guns:
        guns_by_level.get(gun.level, []).append(gun)

    for body in bodies:
        bodies_by_level.get(body.level, []).append(body)

    context = {
        "guns": guns,
        "bodies": bodies,
        "guns_by_level": guns_by_level,
        "bodies_by_level": bodies_by_level,
        "favorite_guns": favorite_guns,
        "favorite_bodies": favorite_bodies,
    }
    return render(request, "information/tanks_info.html", context)


@require_POST
@login_required
def add_gun_comment(request: HttpRequest, gun_id: int) -> JsonResponse:
    text = request.POST.get("text", "").strip()
    if len(text) < 1:
        return JsonResponse({"error": "empty"}, status=400)

    comment = GunComment.objects.create(
        user=request.user,
        gun_id=gun_id,
        text=text,
    )

    return JsonResponse(
        {
            "status": "ok",
            "id": comment.id,
            "user": comment.user.username,
            "text": comment.text,
            "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M"),
        }
    )


@require_POST
@login_required
def delete_gun_comment(request: HttpRequest, comment_id: int) -> JsonResponse:
    comment = GunComment.objects.filter(id=comment_id, user=request.user).first()
    if not comment:
        return JsonResponse({"error": "not_found"}, status=404)

    comment.delete()
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def add_body_comment(request: HttpRequest, body_id: int) -> JsonResponse:
    text = request.POST.get("text", "").strip()
    if len(text) < 1:
        return JsonResponse({"error": "empty"}, status=400)

    comment = BodyComment.objects.create(
        user=request.user,
        body_id=body_id,
        text=text,
    )

    return JsonResponse(
        {
            "status": "ok",
            "id": comment.id,
            "user": comment.user.username,
            "text": comment.text,
            "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M"),
        }
    )


@require_POST
@login_required
def delete_body_comment(request: HttpRequest, comment_id: int) -> JsonResponse:
    comment = BodyComment.objects.filter(id=comment_id, user=request.user).first()
    if not comment:
        return JsonResponse({"error": "not_found"}, status=404)

    comment.delete()
    return JsonResponse({"status": "ok"})


@api_view(["GET"])
def bodies_api(request: HttpRequest) -> Response:
    data = [
        {
            "name": body.name,
            "level": body.level,
            "information": body.information,
            "armor": body.armor,
            "max_speed": body.max_speed,
            "turning_speed": body.turning_speed,
            "weight": body.weight,
            "power": body.power,
        }
        for body in Body.objects.all()
    ]
    return Response(data)


@api_view(["GET"])
def guns_api(request: HttpRequest) -> Response:
    data = [
        {
            "name": gun.name,
            "level": gun.level,
            "information": gun.information,
            "damage_minute": gun.damage_minute,
            "damage": gun.damage,
            "recharge": gun.recharge,
            "ranget": gun.range,
            "power": gun.power,
        }
        for gun in Gun.objects.all()
    ]
    return Response(data)
