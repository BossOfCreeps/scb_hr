from django.db import models


class ResumeStatus(models.TextChoices):
    NEW = "NEW", "Новый"
    SUCCESS = "SUCCESS", "Успешно"
    DENY = "DENY", "Отказ"


class CheckStatus(models.TextChoices):
    NEW = "NEW", "Новый"
    SUCCESS = "SUCCESS", "Успешно"
    DENY = "DENY", "Отказ"
