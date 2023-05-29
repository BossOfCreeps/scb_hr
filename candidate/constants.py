from django.db import models


class ContactType(models.TextChoices):
    EMAIL = "EMAIL", "Почта"
    PHONE = "PHONE", "Телефон"
    ADDRESS = "ADDRESS", "Адрес"
    TELEGRAM = "TELEGRAM", "Telegram"
    VK = "VK", "ВКонтакте"
