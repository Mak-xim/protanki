from django.db import models
from django.conf import settings


class Gun(models.Model):
    LEVEL_CHOICES = [
        ("M0", "M0"),
        ("M1", "M1"),
        ("M2", "M2"),
        ("M3", "M3"),
    ]
    name = models.CharField("name", max_length=50, default="default")
    information = models.TextField("information")
    level = models.CharField("level", max_length=2, choices=LEVEL_CHOICES, default="M0")
    damage_minute = models.FloatField("damage_minute", default=0.0)
    damage = models.FloatField("damage", default=0.0)
    recharge = models.FloatField("recharge", default=0.0)
    range = models.FloatField("range", default=0.0)
    power = models.FloatField("power", default=0.0)
    image = models.ImageField(
        upload_to="guns/", null=True, blank=True
    )  # blank = True -  в формах Django может быть пустым  # null= True - в базе данных поле image может быть пустым

    def __str__(self):
        return (
            self.name
        )  # Когда ты в консоли или в админке Django смотришь список объектов модели, Django вызывает метод __str__ для каждого объекта, чтобы показать его в понятном виде.
        # если этого метода нет, Django показывает что-то вроде <Gun object (1)> — непонятную техническую строку.
        # Благодаря этому методу, объект будет показываться как его имя (то, что хранится в поле name).


class Body(models.Model):
    LEVEL_CHOICES = [
        ("M0", "M0"),
        ("M1", "M1"),
        ("M2", "M2"),
        ("M3", "M3"),
    ]
    name = models.CharField("name", max_length=50, default="default")
    level = models.CharField("level", max_length=2, choices=LEVEL_CHOICES, default="M0")
    information = models.TextField("information", default="default")
    armor = models.FloatField("armor", default=0.0)
    max_speed = models.FloatField("max_speed", default=0.0)
    turning_speed = models.FloatField("turning_speed", default=0.0)
    weight = models.FloatField("weight", default=0.0)
    power = models.FloatField("power", default=0.0)
    image = models.ImageField(
        upload_to="body/", null=True, blank=True
    )  # blank = True -  в формах Django может быть пустым  # null= True - в базе данных поле image может быть пустым


class FavoriteBody(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_bodies_rel",
    )  # on_delete=models.cascade при удалении объекта удаляется связные с ним данные.
    body = models.ForeignKey(
        Body, on_delete=models.CASCADE
    )  # settings.AUTH_USER_MODEL — рекомендуемый способ ссылаться на модель пользователя.
    # Это значение (строка или класс) берётся из django.conf.settings. Используется, чтобы корректно работать с кастомной моделью пользователя.
    # Body ссылается на модель body.

    class Meta:
        unique_together = (
            "user",
            "body",
        )  # unique_together — это ограничение, которое гарантирует уникальность пары (user, body).


# Это значит, что один пользователь не сможет добавить одну и ту же пушку в избранное дважды.
# В базе данных будет запрещено создавать две записи с одинаковым пользователем и одинаковой пушкой.


class FavoriteGun(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_guns_rel",
    )
    gun = models.ForeignKey(Gun, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "gun",
        )  # unique_together — это ограничение, которое гарантирует уникальность пары (user, gun)

    # Это значит, что один пользователь не сможет добавить одну и ту же пушку в избранное дважды.
    # В базе данных будет запрещено создавать две записи с одинаковым пользователем и одинаковой пушкой.


class GunComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gun = models.ForeignKey(Gun, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

class BodyComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.ForeignKey(Body, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]