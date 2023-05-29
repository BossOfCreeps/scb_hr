from django import forms
from django.contrib.auth.models import Permission

from account.models import CustomUser
from helpers.forms import select_multiple_widget, select_widget
from position.constants import PermissionsChoices
from position.models import Position, Organisation


class PermissionModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return PermissionsChoices(obj.codename.upper()).label


class PositionForm(forms.ModelForm):
    organisation = forms.ModelChoiceField(
        queryset=Organisation.objects.all(), to_field_name="id", widget=select_widget, label="Организация"
    )
    permissions = PermissionModelMultipleChoiceField(
        Permission.objects.filter(codename__in=[p.lower() for p in PermissionsChoices]),
        label="Доступы", required=False, widget=select_multiple_widget
    )
    users = forms.ModelMultipleChoiceField(
        CustomUser.objects.all(), to_field_name="id", widget=select_multiple_widget, label="Пользователи",
        required=False
    )

    class Meta:
        model = Position
        fields = "__all__"
