from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import FormView

from helpers.superjob import parse_super_job
from parsing.forms import SuperjobForm


class SuperjobView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = SuperjobForm
    template_name = "parsing/superjob_form.html"
    permission_required = "vacancy.add_vacancy"

    def get_context_data(self, **kwargs):
        data = self.request.GET.dict()

        if data.get("count", "") == "":
            data["count"] = settings.SUPERJOB_PAGE_COUNT
        if data.get("page", "") == "":
            data["page"] = 1

        form = self.form_class(data)
        if form.is_valid():
            total, object_list = parse_super_job(**form.cleaned_data)
            return {"form": form, "object_list": object_list, "total": total}
