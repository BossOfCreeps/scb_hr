import django_filters
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat

from helpers.forms import select_multiple_widget
from inspector.constants import ResumeStatus
from inspector.models import Resume


class ResumeFilter(django_filters.FilterSet):
    position = django_filters.CharFilter("vacancy__position__name", 'icontains', label='Должность')

    full_name = django_filters.CharFilter(label="ФИО", method="full_name_filter")

    status = django_filters.MultipleChoiceFilter(choices=ResumeStatus.choices, widget=select_multiple_widget)

    created__gte = django_filters.DateTimeFilter(label='Создан от', field_name='created', lookup_expr='gte')
    created__gte.field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
    created__lte = django_filters.DateTimeFilter(label='Создан до', field_name='created', lookup_expr='lte')
    created__lte.field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    class Meta:
        model = Resume
        fields = [
            "position",
            'status',
            'full_name',
            "created__gte",
            "created__lte",
        ]

    @staticmethod
    def full_name_filter(queryset, _, value):
        return queryset.annotate(search_name=Concat(
            "candidate__last_name", Value(' '), "candidate__first_name", Value(' '), "candidate__middle_name"
        )).filter(search_name__icontains=value)


class ResumeFilterWithVacancy(ResumeFilter):
    class Meta:
        model = Resume
        fields = [
            "vacancy",
            'status',
            'full_name',
            "created__gte",
            "created__lte",
        ]
