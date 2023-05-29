from django import template

from position.constants import PermissionsChoices

register = template.Library()


@register.filter
def permission_to_label(value):
    return PermissionsChoices(value.codename.upper()).label
