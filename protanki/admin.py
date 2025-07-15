
from django.contrib import admin
from .models import Gun, Body

@admin.register(Gun)
class GunAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'information', 'damage', 'recharge', 'range', 'power', 'damage_minute', 'image')

@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'information', 'armor', 'max_speed', 'turning_speed', 'weight', 'power', 'image')
