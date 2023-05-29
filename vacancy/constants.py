from django.db import models


class WorkYearsEnum(models.TextChoices):
    INTERN = "INTERN", "Без опыта"
    JUNIOR = "JUNIOR", "1-3 года"
    MIDDLE = "MIDDLE", "3-5 лет"
    SENIOR = "SENIOR", "5+ лет"


class EmploymentTypeEnum(models.TextChoices):
    FULL = "FULL", "Полный рабочий день"
    PART = "PART", "Частичная занятость"
    REMOTE = "REMOTE", "Удалённая работа"
    INTERNSHIP = "INTERNSHIP", "Стажировка"
