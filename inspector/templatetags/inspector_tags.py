from django import template
from django.template import RequestContext

from inspector.constants import ResumeStatus
from inspector.models import Resume

register = template.Library()


@register.simple_tag(takes_context=True)
def resumes_to_inspector(context: RequestContext):
    result = 0
    for r in Resume.objects.filter(status=ResumeStatus.NEW):
        if r.check_permission(context.request.user):
            result += 1
    return result
