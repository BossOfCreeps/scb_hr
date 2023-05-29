from django.db import models
from django.urls import reverse

from position.models import Position
from vacancy.constants import EmploymentTypeEnum, WorkYearsEnum


class Specialisation(models.Model):
    name = models.CharField("Название", max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "Специализация вакансии"
        ordering = ["id"]


class WorkYears(models.Model):
    name = models.CharField("Название", max_length=16, choices=WorkYearsEnum.choices, unique=True)

    def __str__(self):
        return WorkYearsEnum(self.name).label

    class Meta:
        verbose_name = verbose_name_plural = "Требуемый опыт"
        ordering = ["id"]


class EmploymentType(models.Model):
    name = models.CharField("Название", max_length=16, choices=EmploymentTypeEnum.choices, unique=True)

    def __str__(self):
        return EmploymentTypeEnum(self.name).label

    class Meta:
        verbose_name = verbose_name_plural = "Тип занятости"
        ordering = ["id"]


class City(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "Город"
        ordering = ["id"]


class Office(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Фотография", null=True, blank=True)

    city = models.ForeignKey(City, models.CASCADE, "offices", verbose_name="город")
    street = models.CharField("Улица", max_length=1024)
    house_number = models.CharField("Дом", max_length=1024)
    office_number = models.CharField("Номер офиса", max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = verbose_name_plural = "Офис"
        ordering = ["id"]


class Vacancy(models.Model):
    position = models.ForeignKey(Position, models.CASCADE, related_name="vacancies", verbose_name="Должность")
    description = models.TextField("Описание", null=True, blank=True)
    specialisations = models.ManyToManyField(Specialisation, "vacancies", verbose_name="Специализация")
    work_years = models.ManyToManyField(WorkYears, "vacancies", verbose_name="Опыт работы")
    employment_types = models.ManyToManyField(EmploymentType, "vacancies", verbose_name="Тип занятости")
    office = models.ForeignKey(Office, models.CASCADE, "vacancies", verbose_name="офис")
    created = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.position} от {self.created.strftime('%d.%m.%Y')}"

    def get_absolute_url(self):
        return reverse('vacancy:vacancy-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = verbose_name_plural = "Вакансия"
        ordering = ["id"]


class VacancyCheck(models.Model):
    vacancy = models.ForeignKey(Vacancy, models.CASCADE, "checks", verbose_name="Вакансия")
    inspectors = models.ManyToManyField(Position, "as_inspector", verbose_name="Должности, которые могут согласовать")
    description = models.TextField("Описание", null=True, blank=True)
    visible_for_candidate = models.BooleanField("Видим для кандидата", default=True)

    def __str__(self):
        return f"{self.vacancy} ({self.description if self.description else '-'})"

    def get_absolute_url(self):
        return reverse('vacancy:vacancy-detail', kwargs={'pk': self.vacancy_id})

    class Meta:
        verbose_name = verbose_name_plural = "Проверка вакансии"
        ordering = ["id"]
