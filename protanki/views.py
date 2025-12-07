from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import FavoriteGun, FavoriteBody, Gun, Body, GunComment, BodyComment
from .utils import calculate_gun_percentages, calculate_body_percentages


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

    favorite_guns_qs = FavoriteGun.objects.filter(user=request.user).select_related("gun")
    favorite_bodies_qs = FavoriteBody.objects.filter(user=request.user).select_related("body")

    favorite_guns = [fav.gun for fav in favorite_guns_qs]
    favorite_bodies = [fav.body for fav in favorite_bodies_qs]

    if search_query:
        favorite_guns = [
            gun for gun in favorite_guns
            if search_query in gun.name.lower() or search_query in gun.information.lower()
        ]
        favorite_bodies = [
            body for body in favorite_bodies
            if search_query in body.name.lower() or search_query in body.information.lower()
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
        favorite_guns = set(request.user.favorite_guns_rel.values_list("gun_id", flat=True))
    else:
        favorite_guns = set()

    if request.user.is_authenticated and hasattr(request.user, "favorite_bodies_rel"):
        favorite_bodies = set(request.user.favorite_bodies_rel.values_list("body_id", flat=True))
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
def add_gun_comment(request, gun_id):
    text = request.POST.get("text", "").strip()
    if len(text) < 1:
        return JsonResponse({"error": "empty"}, status=400)

    comment = GunComment.objects.create(
        user=request.user,
        gun_id=gun_id,
        text=text,
    )

    return JsonResponse({
        "status": "ok",
        "id": comment.id,
        "user": comment.user.username,
        "text": comment.text,
        "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M")
    })

@require_POST
@login_required
def delete_gun_comment(request, comment_id):
    comment = GunComment.objects.filter(id=comment_id, user=request.user).first()
    if not comment:
        return JsonResponse({"error": "not_found"}, 404)

    comment.delete()
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def add_body_comment(request, body_id):
    text = request.POST.get("text", "").strip()
    if len(text) < 1:
        return JsonResponse({"error": "empty"}, status=400)

    comment = BodyComment.objects.create(
        user=request.user,
        body_id=body_id,
        text=text,
    )

    return JsonResponse({
        "status": "ok",
        "id": comment.id,
        "user": comment.user.username,
        "text": comment.text,
        "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M")
    })


@require_POST
@login_required
def delete_body_comment(request, comment_id):
    comment = BodyComment.objects.filter(id=comment_id, user=request.user).first()
    if not comment:
        return JsonResponse({"error": "not_found"}, 404)

    comment.delete()
    return JsonResponse({"status": "ok"})


# --- КОРПУСА ---