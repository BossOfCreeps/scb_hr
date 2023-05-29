from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView

from archive.filters import ArchiveFilter
from helpers.excel import create_resumes_xlsx
from inspector.models import Resume


class ArchiveListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Resume
    template_name = "archive/archive_list.html"
    permission_required = "inspector.view_resume"

    def get_context_data(self, **kwargs):
        return {
            "resumes": ArchiveFilter(self.request.GET).qs,
            "filter": ArchiveFilter(self.request.GET),
            "show_filter": set(self.request.GET.dict().values()) not in [{""}, set()],
        }


class ArchiveDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Resume
    template_name = "archive/archive_detail.html"
    permission_required = "inspector.view_resume"

    def get_context_data(self, **kwargs):
        vacancy_checks = self.get_object().vacancy.checks.all()
        resume_checks = self.get_object().checks.all()

        return {
            "resume": self.get_object(),
            "checks": [
                {
                    "vacancy": vacancy_checks[i],
                    "resume": resume_checks[i] if len(resume_checks) > i else None,
                }
                for i in range(len(vacancy_checks))
            ],
        }


class ArchiveDownload(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.view_resume"

    def get(self, request):
        response = HttpResponse(create_resumes_xlsx(ArchiveFilter(self.request.GET).qs))
        response['Content-Disposition'] = f'attachment; filename="resumes_report_{datetime.now().isoformat()}.xls"'
        return response
