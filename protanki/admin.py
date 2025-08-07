
from django.contrib import admin
from .models import Gun, Body, FavoriteGun, FavoriteBody


@admin.register(Gun)
class GunAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    fields = ('name', 'level', 'information', 'damage', 'damage_minute', 'recharge', 'range', 'power', 'image')

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    fields = ('name', 'level', 'information', 'armor', 'max_speed', 'turning_speed', 'weight', 'power', 'image')

@admin.register(FavoriteGun)
class FavoriteGunAdmin(admin.ModelAdmin):
    list_display = ('user', 'gun_name', 'damage', 'recharge', 'power')

    def gun_name(self, obj):
        return obj.gun.name
    gun_name.short_description = 'Пушка'

    def damage(self, obj):
        return obj.gun.damage
    damage.short_description = 'Урон'

    def recharge(self, obj):
        return obj.gun.recharge
    recharge.short_description = 'Перезарядка'

    def power(self, obj):
        return obj.gun.power
    power.short_description = 'Сила удара'

@admin.register(FavoriteBody)
class FavoriteBodyAdmin(admin.ModelAdmin):
    list_display = ('user', 'body_name', 'armor', 'max_speed', 'weight')

    def body_name(self, obj):
        return obj.body.name
    body_name.short_description = 'Корпус'

    def armor(self, obj):
        return obj.body.armor
    armor.short_description = 'Броня'

    def max_speed(self, obj):
        return obj.body.max_speed
    max_speed.short_description = 'Макс. скорость'

    def weight(self, obj):
        return obj.body.weight
    weight.short_description = 'Масса'


