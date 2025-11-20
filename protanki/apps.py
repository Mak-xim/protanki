from django.apps import (
    AppConfig,
)  # Мы импортируем базовый класс AppConfig из модуля django.apps. Этот класс нужен, чтобы создать свою конфигурацию приложения.


class ProtankiConfig(
    AppConfig
):  # cоздаём класс ProtankiConfig, который наследуется от AppConfig. Это значит, что ProtankiConfig — это именно конфигурация приложения.
    default_auto_field = "django.db.models.BigAutoField"
    name = "protanki"
    # default_auto_field = "django.db.models.BigAutoField"
    #
    # Эта настройка говорит Django, что по умолчанию для всех моделей в приложении protanki нужно использовать тип поля для первичного ключа (primary key) — BigAutoField.
    #
    # BigAutoField — это числовое поле, которое автоматически увеличивается при добавлении новых записей.
    #
    # В отличие от обычного AutoField, BigAutoField использует 64-битные числа, то есть может хранить гораздо больше значений (нужно для больших баз данных).
    #
    # Задавая это в конфигурации, мы не пишем id = models.BigAutoField(primary_key=True) в каждой модели — Django сделает это автоматически.
    #
    # name = "protanki"
    #
    # Это имя приложения — строка, которая должна совпадать с названием папки/приложения в проекте.
    #
    # Django использует это имя для поиска приложения, связывания его с конфигурацией и других внутренних целей.
