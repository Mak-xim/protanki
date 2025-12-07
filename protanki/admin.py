from django.contrib import admin

from .models import Body, BodyComment, FavoriteBody, FavoriteGun, Gun


@admin.register(
    Gun
)  # @admin.register(Gun) — декоратор, регистрирующий модель Gun в админке с указанным классом настроек.
#  декоратор — это специальная функция, которая "оборачивает" другую функцию или метод, изменяя или добавляя к нему поведение, не меняя его код напрямую.
# другие декораторы
# @permission_required('app_name.permission_code') — проверка прав доступа.
#
# @require_http_methods(["GET", "POST"]) — ограничивает допустимые HTTP-методы.
#
# @csrf_exempt — отключает CSRF-проверку для view.
class GunAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
    )  # list_display — определяет, какие поля будут показаны в списке объектов.
    fields = (
        "name",
        "level",
        "information",
        "damage",
        "damage_minute",
        "recharge",
        "range",
        "power",
        "image",
    )  # fields — определяет порядок и набор полей в форме редактирования/создания объекта в админке.


@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ("name", "level")
    fields = (
        "name",
        "level",
        "information",
        "armor",
        "max_speed",
        "turning_speed",
        "weight",
        "power",
        "image",
    )


@admin.register(FavoriteGun)
class FavoriteGunAdmin(admin.ModelAdmin):
    list_display = ("user", "gun_name")

    def gun_name(self, obj):  # self — это экземпляр админ-класса (FavoriteGunAdmin).
        return (
            obj.gun.name
        )  # obj — это объект FavoriteGun. # obj.gun — это связанная модель Gun (ForeignKey в FavoriteGun). #.name — берём название пушки.

    gun_name.short_description = (
        "Пушка"  # short_description — название колонки в админке.
    )

    def damage(self, obj):
        return obj.gun.damage

    damage.short_description = "Урон"

    def recharge(self, obj):
        return obj.gun.recharge

    recharge.short_description = "Перезарядка"

    def power(self, obj):
        return obj.gun.power

    power.short_description = "Сила удара"

    def image(self, obj):
        return obj.image.url

    image.short_description = "Картинка"


@admin.register(FavoriteBody)
class FavoriteBodyAdmin(admin.ModelAdmin):
    list_display = ("user", "body_name")

    def body_name(self, obj):
        return obj.body.name

    body_name.short_description = "Корпус"

    def armor(self, obj):
        return obj.body.armor

    armor.short_description = "Броня"

    def max_speed(self, obj):
        return obj.body.max_speed

    max_speed.short_description = "Макс. скорость"

    def weight(self, obj):
        return obj.body.weight

    weight.short_description = "Масса"


@admin.register(BodyComment)
class BodyCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "body", "created_at")
