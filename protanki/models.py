from django.db import models


class Gun(models.Model):
    name = models.CharField("name", max_length=50, default="default")
    information = models.TextField("information")
    damage_minute = models.FloatField("damage_minute", default=0.0)
    damage = models.FloatField("damage", default=0.0)
    recharge = models.FloatField("recharge", default=0.0)
    range = models.FloatField("range", default=0.0)
    power = models.FloatField("power", default=0.0)
    image = models.ImageField(upload_to='guns/', null=True, blank=True)

    def __str__(self):
        return self.name

class Body(models.Model):
    name = models.CharField("name", max_length=50, default="default")
    information = models.TextField("information")
    armor = models.FloatField("armor")
    max_speed = models.FloatField("max_speed")
    turning_speed = models.FloatField("turning_speed")
    weight = models.FloatField("weight")
    power = models.FloatField("power")
    image = models.ImageField(upload_to='body/', null=True, blank=True)

    def __str__(self):
        return self.name




