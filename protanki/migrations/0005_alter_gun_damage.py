# Generated by Django 5.2.4 on 2025-07-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("protanki", "0004_alter_gun_damage_minute"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gun",
            name="damage",
            field=models.FloatField(default=0, verbose_name="damage"),
        ),
    ]
