from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from account.models import CustomUser
from candidate.constants import ContactType
from position.models import Position


class WorkExperience(models.Model):
    candidate = models.ForeignKey(CustomUser, models.CASCADE, "work_experiences", verbose_name="Резюме")

    start_date = models.DateField("Начало работы")
    finish_date = models.DateField("Конец работы", blank=True, null=True)

    company = models.CharField("Организация", max_length=1024)
    position = models.CharField("Должность", max_length=1024)
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return f"{self.candidate} ({self.company})"

    @staticmethod
    def get_absolute_url():
        return reverse('candidate:candidate-profile')

    class Meta:
        verbose_name = verbose_name_plural = "Опыт работы"
        ordering = ["id"]


class Education(models.Model):
    candidate = models.ForeignKey(CustomUser, models.CASCADE, "educations", verbose_name="Резюме")

    place = models.CharField("Заведение", max_length=1024)
    direction = models.CharField("Направление", max_length=1024)

    start_date = models.DateField("Начало обучения")
    finish_date = models.DateField("Конец обучения", blank=True, null=True)

    def __str__(self):
        return f"{self.candidate} ({self.place})"

    @staticmethod
    def get_absolute_url():
        return reverse('candidate:candidate-profile')

    class Meta:
        verbose_name = verbose_name_plural = "Запись об образовании"
        ordering = ["id"]


class Contact(models.Model):
    candidate = models.ForeignKey(CustomUser, models.CASCADE, "contacts", verbose_name="Кандидат")

    type = models.CharField("Тип", max_length=8, choices=ContactType.choices)
    value = models.CharField("Значение", max_length=32)

    def __str__(self):
        return f"{self.value} ({self.type})"

    @staticmethod
    def get_absolute_url():
        return reverse('candidate:candidate-profile')

    class Meta:
        verbose_name = verbose_name_plural = "Контакт"
        ordering = ["id"]
