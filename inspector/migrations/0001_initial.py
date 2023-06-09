# Generated by Django 4.2.1 on 2023-05-26 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vacancy", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "Новый"),
                            ("SUCCESS", "Успешно"),
                            ("DENY", "Отказ"),
                        ],
                        default="NEW",
                        max_length=16,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "cv",
                    models.TextField(
                        blank=True, null=True, verbose_name="Сопроводительное письмо"
                    ),
                ),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Кандидат",
                    ),
                ),
                (
                    "vacancy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resumes",
                        to="vacancy.vacancy",
                        verbose_name="Вакансия",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResumeFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="", verbose_name="Файл")),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="inspector.resume",
                        verbose_name="Резюме",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResumeCheck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "Новый"),
                            ("SUCCESS", "Успешно"),
                            ("DENY", "Отказ"),
                        ],
                        default="NEW",
                        max_length=16,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checks",
                        to="inspector.resume",
                        verbose_name="Резюме",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь. который проверял",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Interview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(verbose_name="Дата начала интервью"),
                ),
                (
                    "finish_date",
                    models.DateTimeField(verbose_name="Дата окончания интервью"),
                ),
                ("url", models.URLField(blank=True, null=True, verbose_name="Ссылка")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="interviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Участники",
                    ),
                ),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interviews",
                        to="inspector.resume",
                        verbose_name="Резюме",
                    ),
                ),
            ],
        ),
    ]
