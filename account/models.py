from typing import Optional, List, Tuple

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from candidate.constants import ContactType
from scb_hr.celery import async_send_email, async_send_telegram


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)

    last_name = models.CharField("Фамилия", max_length=1024)
    first_name = models.CharField("Имя", max_length=1024)
    middle_name = models.CharField("Отчество", max_length=1024, null=True, blank=True)
    image = models.ImageField("Фотография", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def has_perm(self, perm: str, obj=None):
        permissions = [permission for position in self.positions.all() for permission in position.permissions.all()]
        return self.is_superuser or perm in [f"{p.content_type.app_label}.{p.codename}" for p in permissions]

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name if self.middle_name else ''}".strip()

    @staticmethod
    def get_absolute_url():
        return reverse('candidate:candidate-profile')

    def send_message(self, title: str, text: str, files_data: Optional[List[Tuple[str, str]]] = None):
        contacts = {(ContactType(contact.type), contact.value) for contact in self.contacts.all()}
        contacts.add((ContactType.EMAIL, self.email))

        for contact_type, value in contacts:
            if contact_type == ContactType.EMAIL:
                async_send_email.delay(value, title, text, files_data)

            elif contact_type == ContactType.PHONE:
                pass  # BACKLOG: смс

            elif contact_type == ContactType.TELEGRAM:
                tg_user = TelegramUser.objects.filter(username=value.lower()).first()
                if tg_user:
                    async_send_telegram.delay(tg_user.tg_id, f"{title}\n\n{text}", files_data)

                elif contact_type == ContactType.VK:
                    pass  # BACKLOG: вконтакте

    class Meta:
        verbose_name = verbose_name_plural = "Пользователь"
        ordering = ["id"]


class EmailValidation(models.Model):
    email = models.EmailField()
    value = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.email} : {self.value}"

    class Meta:
        verbose_name = verbose_name_plural = "Код проверки почты"
        ordering = ["id"]


class TelegramUser(models.Model):
    username = models.CharField(max_length=1024)
    tg_id = models.IntegerField()

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = verbose_name_plural = "Telegram пользователь"
        ordering = ["id"]
