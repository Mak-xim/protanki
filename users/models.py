from django.contrib.auth.models import AbstractUser
from django.db import models
from protanki.models import Gun, Body

class CustomUser(AbstractUser):
    email = models.EmailField(unique=False, blank=False, null=True, verbose_name="Email")
    first_name = models.CharField(blank=True, null=True, max_length=100, verbose_name="Имя")
    last_name = models.CharField(blank=True, null=True, max_length=100, verbose_name="Фамилия")


    def __str__(self):
        return self.username