from django.contrib.auth.models import Permission
from django.db import models
from django.urls import reverse

from account.models import CustomUser


class Organisation(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "Организация"
        ordering = ["id"]


class Position(models.Model):
    name = models.CharField("Должность", max_length=1024)
    organisation = models.ForeignKey(Organisation, models.CASCADE, "positions", verbose_name="организация")
    permissions = models.ManyToManyField(Permission, "positions", verbose_name="доступы", blank=True)
    users = models.ManyToManyField(CustomUser, "positions", blank=True, verbose_name="Пользователи")

    def __str__(self):
        return f"{self.name} ({self.organisation})"

    @staticmethod
    def get_absolute_url():
        return reverse('position:position-list')

    class Meta:
        verbose_name = verbose_name_plural = "Должность"
        ordering = ["id"]
