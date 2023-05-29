from django.db import models


class PermissionsChoices(models.TextChoices):
    CHANGE_RESUME = "CHANGE_RESUME", "Согласовывать резюме"
    ADD_INTERVIEW = "ADD_INTERVIEW", "Создавать интервью"
    VIEW_RESUME = "VIEW_RESUME", "Работать с архивом резюме"
    CHANGE_VACANCY = "CHANGE_VACANCY", "Полный доступ к вакансиям"
    CHANGE_POSITION = "CHANGE_POSITION", "Полный доступ к должностям"
    ADD_VACANCY = "ADD_VACANCY", "Парсинг резюме"
    ADD_RESUME = "ADD_RESUME", "Работать с отчётами"
