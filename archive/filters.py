import django_filters
from django import forms
from django.db.models import Value, QuerySet, Q
from django.db.models.functions import Concat

from helpers.forms import select_multiple_widget
from inspector.constants import ResumeStatus, CheckStatus
from inspector.models import Resume


class ArchiveFilter(django_filters.FilterSet):
    position = django_filters.CharFilter("vacancy__position__name", 'icontains', label='Должность')

    full_name = django_filters.CharFilter(label="ФИО", method="full_name_filter")
    status = django_filters.MultipleChoiceFilter(choices=ResumeStatus.choices, widget=select_multiple_widget)

    created__gte = django_filters.DateTimeFilter(label='Создан от', field_name='created', lookup_expr='gte')
    created__gte.field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
    created__lte = django_filters.DateTimeFilter(label='Создан до', field_name='created', lookup_expr='lte')
    created__lte.field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    work_experience_company = django_filters.CharFilter(
        label="Бывшие места работы (организации)", method="work_experience_company_filter"
    )
    work_experience_position = django_filters.CharFilter(
        label="Бывшие места работы (позиция и описание)", method="work_experience_position_filter"
    )
    work_experience_start_date = django_filters.DateFilter(
        label='Бывшие места работы (работал от)', method="work_experience_date_filter"
    )
    work_experience_start_date.field.widget = forms.DateInput(attrs={'type': 'date'})
    work_experience_finish_date = django_filters.DateFilter(
        label='Бывшие места работы (работал до)', method="work_experience_date_filter"
    )
    work_experience_finish_date.field.widget = forms.DateInput(attrs={'type': 'date'})

    education_place = django_filters.CharFilter(label="Образование (место)", method="education_place_filter")
    education_direction = django_filters.CharFilter(
        label="Образование (направление)", method="education_direction_filter"
    )
    education_start_date = django_filters.DateFilter(
        label='Образование (старт обучения)', method="education_date_filter"
    )
    education_start_date.field.widget = forms.DateInput(attrs={'type': 'date'})
    education_finish_date = django_filters.DateFilter(
        label='Образование (конец обучения)', method="education_date_filter"
    )
    education_finish_date.field.widget = forms.DateInput(attrs={'type': 'date'})

    deny_description = django_filters.CharFilter(
        label="Причина отказа (только для отклонённых)", method="deny_description_filter"
    )

    class Meta:
        model = Resume
        fields = ["position", 'status', 'full_name', "created__gte", "created__lte"]

    @staticmethod
    def full_name_filter(queryset, _, value):
        return queryset.annotate(search_name=Concat(
            "candidate__last_name", Value(' '), "candidate__first_name", Value(' '), "candidate__middle_name"
        )).filter(search_name__icontains=value)

    def work_experience_company_filter(self, queryset: QuerySet[Resume], _, value):
        resume_ids = []
        for resume in queryset:
            q = resume.candidate.work_experiences.filter(company__icontains=value)
            if self.data.get("work_experience_start_date"):  # noqa
                q = q.filter(
                    start_date__lte=self.data.get("work_experience_start_date"),
                    finish_date__gte=self.data.get("work_experience_start_date"),
                )
            if self.data.get("work_experience_finish_date"):
                q = q.filter(
                    start_date__lte=self.data.get("work_experience_finish_date"),
                    finish_date__gte=self.data.get("work_experience_finish_date"),
                )
            if q.count():
                resume_ids.append(resume.id)

        return queryset.filter(id__in=resume_ids)

    def work_experience_position_filter(self, queryset: QuerySet[Resume], _, value):
        resume_ids = []
        for resume in queryset:
            q = resume.candidate.work_experiences.filter(Q(position__icontains=value) | Q(description__icontains=value))
            if self.data.get("work_experience_start_date"):  # noqa
                q = q.filter(
                    start_date__lte=self.data.get("work_experience_start_date"),
                    finish_date__gte=self.data.get("work_experience_start_date"),
                )
            if self.data.get("work_experience_finish_date"):
                q = q.filter(
                    start_date__lte=self.data.get("work_experience_finish_date"),
                    finish_date__gte=self.data.get("work_experience_finish_date"),
                )
            if q.count():
                resume_ids.append(resume.id)

        return queryset.filter(id__in=resume_ids)

    @staticmethod
    def work_experience_date_filter(queryset, _, value):
        return queryset.filter(id__in=[
            resume.id
            for resume in queryset
            if resume.candidate.work_experiences.filter(start_date__lte=value, finish_date__gte=value).count()
        ])

    def education_place_filter(self, queryset, _, value):
        resume_ids = []  # noqa
        for resume in queryset:
            q = resume.candidate.educations.filter(place__icontains=value)
            if self.data.get("education_start_date"):  # noqa
                q = q.filter(
                    start_date__lte=self.data.get("education_start_date"),
                    finish_date__gte=self.data.get("education_start_date"),
                )
            if self.data.get("education_finish_date"):
                q = q.filter(
                    start_date__lte=self.data.get("education_finish_date"),
                    finish_date__gte=self.data.get("education_finish_date"),
                )
            if q.count():
                resume_ids.append(resume.id)

        return queryset.filter(id__in=resume_ids)

    def education_direction_filter(self, queryset, _, value):
        resume_ids = []  # noqa
        for resume in queryset:
            q = resume.candidate.educations.filter(direction__icontains=value)
            if self.data.get("education_start_date"):  # noqa
                q = q.filter(
                    start_date__lte=self.data.get("education_start_date"),
                    finish_date__gte=self.data.get("education_start_date"),
                )
            if self.data.get("education_finish_date"):
                q = q.filter(
                    start_date__lte=self.data.get("education_finish_date"),
                    finish_date__gte=self.data.get("education_finish_date"),
                )
            if q.count():
                resume_ids.append(resume.id)
        return queryset.filter(id__in=resume_ids)

    @staticmethod
    def education_date_filter(queryset, _, value):
        return queryset.filter(id__in=[
            resume.id
            for resume in queryset
            if resume.candidate.educations.filter(start_date__lte=value, finish_date__gte=value).count()
        ])

    @staticmethod
    def deny_description_filter(queryset, _, value):
        return queryset.filter(id__in=[
            resume.id
            for resume in queryset
            if resume.checks.filter(status=CheckStatus.DENY, description__icontains=value).count()
        ])
