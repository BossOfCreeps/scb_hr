from django import forms

from helpers.forms import select_multiple_widget, select_widget
from position.models import Position
from vacancy.models import Vacancy, VacancyCheck, Specialisation, WorkYears, EmploymentType, Office


class VacancyForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(), to_field_name="id", widget=select_widget, label="Должность"
    )
    work_years = forms.ModelMultipleChoiceField(
        queryset=WorkYears.objects.all(), to_field_name="id", widget=select_multiple_widget, label="Опыт работы"
    )
    employment_types = forms.ModelMultipleChoiceField(
        queryset=EmploymentType.objects.all(), to_field_name="id", widget=select_multiple_widget, label="Тип занятости"
    )
    specialisations = forms.ModelMultipleChoiceField(
        queryset=Specialisation.objects.all(), to_field_name="id", widget=select_multiple_widget, label="Специализация"
    )
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(), to_field_name="id", widget=select_widget, label="Офис"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCheckForm(forms.ModelForm):
    inspectors = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(), to_field_name="id", widget=select_multiple_widget,
        label="Должности, которые могут согласовать"
    )

    class Meta:
        model = VacancyCheck
        fields = ["inspectors", "description", "visible_for_candidate"]
