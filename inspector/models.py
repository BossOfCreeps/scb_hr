from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import Http404
from django.urls import reverse

from account.models import CustomUser
from helpers.ics import create_ics
from inspector.constants import ResumeStatus, CheckStatus
from vacancy.models import Vacancy, VacancyCheck


class Resume(models.Model):
    vacancy = models.ForeignKey(Vacancy, models.CASCADE, "resumes", verbose_name="Вакансия")
    status = models.CharField("Статус", max_length=16, choices=ResumeStatus.choices, default=ResumeStatus.NEW)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    candidate = models.ForeignKey(CustomUser, models.CASCADE, "resumes", verbose_name="Кандидат")
    cv = models.TextField("Сопроводительное письмо", null=True, blank=True)

    def __str__(self):
        return f"{self.vacancy.position} / {self.candidate} / {self.created.isoformat()}"

    @staticmethod
    def get_absolute_url():
        return reverse('candidate:candidate-profile')

    def check_permission(self, user: CustomUser) -> bool:
        if self.status != ResumeStatus.NEW:
            return False

        needed_checks = self.vacancy.checks.all()
        done_checks = self.checks.all()

        if len(done_checks) >= len(needed_checks):
            return False

        check: VacancyCheck = needed_checks[len(done_checks)]
        for user_position in user.positions.all():
            for check_position in check.inspectors.all():
                if check_position == user_position:
                    return True

        return False

    def approve(self, user: CustomUser, description: Optional[str] = ""):
        if not self.check_permission(user):
            raise Http404()

        if description is None:
            description = ""

        ResumeCheck.objects.create(resume=self, user=user, status=CheckStatus.SUCCESS, description=description)

        self.candidate.send_message(
            "Результат собеседования: ещё один шажок пройден",
            f"Поздравляем. Вы ещё немного ближе к оферу.\n{description}"
        )

        if self.checks.count() == self.vacancy.checks.count():
            self.status = ResumeStatus.SUCCESS
            self.save()

            self.candidate.send_message(
                "Результат собеседования: победа",
                "Ура! Вы прошли. Скоро с вами свяжутся для уточнения данных"
            )

    def deny(self, user: CustomUser, description: str = ""):
        if not self.check_permission(user):
            raise Http404()

        ResumeCheck.objects.create(resume=self, user=user, status=CheckStatus.DENY, description=description)

        self.status = ResumeStatus.DENY
        self.save()

        self.candidate.send_message(
            "Результат собеседования: отказ",
            f"К сожалению, мы вынуждены вам отказать.\n{description}",
        )

    class Meta:
        verbose_name = verbose_name_plural = "Резюме"
        ordering = ["id"]


class ResumeFile(models.Model):
    resume = models.ForeignKey(Resume, models.CASCADE, "files", verbose_name="Резюме")
    file = models.FileField("Файл")

    def __str__(self):
        return f"{self.resume} ({self.file})"

    class Meta:
        verbose_name = verbose_name_plural = "Файл резюме"
        ordering = ["id"]


class ResumeCheck(models.Model):
    resume = models.ForeignKey(Resume, models.CASCADE, "checks", verbose_name="Резюме")
    user = models.ForeignKey(CustomUser, models.CASCADE, "checks", verbose_name="Пользователь. который проверял")
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    status = models.CharField("Статус", max_length=16, choices=CheckStatus.choices, default=CheckStatus.NEW)
    description = models.TextField("Описание", null=True, blank=True)

    def __str__(self):
        return f"{self.description} / {self.resume} / {self.user}"

    class Meta:
        verbose_name = verbose_name_plural = "Проверка резюме"
        ordering = ["id"]


class Interview(models.Model):
    resume = models.ForeignKey(Resume, models.CASCADE, "interviews", verbose_name="Резюме")
    participants = models.ManyToManyField(CustomUser, "interviews", verbose_name="Участники")
    start_date = models.DateTimeField("Дата начала интервью")
    finish_date = models.DateTimeField("Дата окончания интервью")
    url = models.URLField("Ссылка", blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return f"{self.resume} ({self.start_date.isoformat()})"

    def __send_messages(self, title):
        ics = self.generate_ics()

        for user in set([user for user in self.participants.all()] + [self.resume.candidate]):
            user.send_message(
                title,
                f"Описание: {self.description}\n"
                + (f"Ссылка: {self.url}\n" if self.url else "")
                + f"Дата начала: {self.start_date.strftime('%H:%M %d.%m.%Y')}, "
                  f"дата окончания {self.finish_date.strftime('%H:%M %d.%m.%Y')}\n",
                [("event.ics", ics.decode())]
            )

    def send_creation_messages(self):
        self.__send_messages(
            f"Назначено собеседование на позицию {self.resume.vacancy.position.name} "
            f"для {self.resume.candidate.full_name}"
        )

    def send_reminder_messages(self):
        self.__send_messages(
            f"Напоминаем о собеседовании на позицию {self.resume.vacancy.position.name} "
            f"для {self.resume.candidate.full_name}",
        )

    def generate_ics(self) -> bytes:
        return create_ics(
            f"Назначено собеседование на позицию {self.resume.vacancy.position.name}",
            self.start_date,
            self.finish_date,
            f"Описание: {self.description}\n" + f"Ссылка: {self.url}" if self.url else "",
            [user.email for user in self.participants.all()]
        )

    @staticmethod
    def get_absolute_url():
        return reverse('inspector:resume-list')

    class Meta:
        verbose_name = verbose_name_plural = "Интервью"
        ordering = ["id"]
