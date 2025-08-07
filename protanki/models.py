from django.db import models
from django.conf import settings


class Gun(models.Model):
    LEVEL_CHOICES = [
        ('M0', 'M0'),
        ('M1', 'M1'),
        ('M2', 'M2'),
        ('M3', 'M3'),
    ]
    name = models.CharField("name", max_length=50, default="default")
    information = models.TextField("information")
    level = models.CharField("level", max_length=2, choices=LEVEL_CHOICES, default="M0")
    damage_minute = models.FloatField("damage_minute", default=0.0)
    damage = models.FloatField("damage", default=0.0)
    recharge = models.FloatField("recharge", default=0.0)
    range = models.FloatField("range", default=0.0)
    power = models.FloatField("power", default=0.0)
    image = models.ImageField(upload_to='guns/', null=True, blank=True)

    def __str__(self):
        return self.name

class Body(models.Model):
    LEVEL_CHOICES = [
        ('M0', 'M0'),
        ('M1', 'M1'),
        ('M2', 'M2'),
        ('M3', 'M3'),
    ]
    name = models.CharField("name", max_length=50, default="default")
    level = models.CharField("level", max_length=2, choices=LEVEL_CHOICES, default="M0")
    information = models.TextField("information", default=0.0)
    armor = models.FloatField("armor", default=0.0)
    max_speed = models.FloatField("max_speed", default=0.0)
    turning_speed = models.FloatField("turning_speed", default=0.0)
    weight = models.FloatField("weight", default=0.0)
    power = models.FloatField("power", default=0.0)
    image = models.ImageField(upload_to='body/', null=True, blank=True)

    def __str__(self):
        return self.name

class FavoriteGun(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_guns_rel')
    gun = models.ForeignKey('protanki.Gun', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'gun')

class FavoriteBody(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_bodies_rel')
    body = models.ForeignKey('protanki.Body', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'body')




