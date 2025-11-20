from typing import List

def calculate_gun_percentages(guns: List):
    """Добавляет проценты характеристик пушек для отображения прогресс-баров."""
    for gun in guns:
        gun.damage_percent = min(int(gun.damage / 68 * 100), 100)
        gun.dpm_percent = min(int(gun.damage_minute / 187 * 100), 100)
        gun.recharge_percent = min(int(gun.recharge / 15 * 100), 100)
        gun.range_percent = min(int(gun.range / 150 * 100), 100)
        gun.power_percent = min(int(gun.power / 369 * 100), 100)
    return guns

def calculate_body_percentages(bodies: List):
    """Добавляет проценты характеристик корпусов для отображения прогресс-баров."""
    for body in bodies:
        body.armor_percent = min(int(body.armor / 1000 * 100), 100)
        body.max_speed_percent = min(int(body.max_speed / 10000 * 100), 100)
        body.turning_speed_percent = min(int(body.turning_speed / 10 * 100), 100)
        body.weight_percent = min(int(body.weight / 1000 * 100), 100)
        body.power_percent = min(int(body.power / 100 * 100), 100)
    return bodies