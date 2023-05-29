import django_filters
from django.db.models import Q

from helpers.forms import select_multiple_widget
from vacancy.models import Vacancy, City, EmploymentType, WorkYears, Specialisation


class VacancyFilter(django_filters.FilterSet):
    city = django_filters.ModelMultipleChoiceFilter(
        queryset=City.objects.all(), field_name="office__city", label="Город", widget=select_multiple_widget
    )
    text = django_filters.CharFilter(label="Должность", method="text_filter")

    work_years = django_filters.ModelMultipleChoiceFilter(
        queryset=WorkYears.objects.all(), to_field_name="id", widget=select_multiple_widget
    )
    employment_types = django_filters.ModelMultipleChoiceFilter(
        queryset=EmploymentType.objects.all(), to_field_name="id", widget=select_multiple_widget
    )
    specialisations = django_filters.ModelMultipleChoiceFilter(
        queryset=Specialisation.objects.all(), to_field_name="id", widget=select_multiple_widget
    )

    class Meta:
        model = Vacancy
        fields = ["city", "text", "work_years", "employment_types", "specialisations"]

    @staticmethod
    def text_filter(qs, _, value):
        return qs.filter(Q(position__name__icontains=value) | Q(description__icontains=value))
