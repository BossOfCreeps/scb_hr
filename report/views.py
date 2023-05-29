from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, FormView

from inspector.constants import ResumeStatus
from inspector.filters import ResumeFilter, ResumeFilterWithVacancy
from inspector.models import Resume
from report.filters import ResumeFilterWithoutPosition, ResumeFilterWithoutDate, ResumeFilterWithoutStatus
from vacancy.models import Vacancy


class ResumePerVacancyReportView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "report/resume_per_vacancy.html"
    permission_required = "inspector.add_resume"

    def get_context_data(self, **kwargs):
        return {
            "form": ResumeFilterWithoutPosition(self.request.GET).form,
            "vacancies": Vacancy.objects.all(),
        }


class ResumePerVacancyReportAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.add_resume"

    def post(self, request):
        data = self.request.POST.dict()

        return JsonResponse(
            [
                ResumeFilterWithVacancy(data | {"vacancy": vacancy, "status": data["status"].split()}).qs.count()
                for vacancy in Vacancy.objects.all()
            ], safe=False
        )


class ResumePerDatetimeReportView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "report/resume_per_datetime.html"
    permission_required = "inspector.add_resume"

    def get_context_data(self, **kwargs):
        return {"form": ResumeFilterWithoutDate(self.request.GET).form}


class ResumePerDatetimeReportAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.add_resume"

    def post(self, request):
        data = self.request.POST.dict()
        dates = sorted([resume.created.date() for vacancy in Vacancy.objects.all() for resume in vacancy.resumes.all()])
        return JsonResponse(
            [
                (
                    datetime(date.year, date.month, date.day, 0, 0, 0, 0).timestamp(),
                    ResumeFilter(
                        data | {"status": data["status"].split()}, Resume.objects.filter(created__date=date)
                    ).qs.count(),
                )
                for date in dates
            ], safe=False
        )


class ResumeStatusPieReportView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "report/resume_pie.html"
    permission_required = "inspector.add_resume"

    def get_context_data(self, **kwargs):
        return {
            "form": ResumeFilterWithoutStatus(self.request.GET).form,
            "resume_statuses": ResumeStatus,
        }


class ResumeStatusPieReportAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.add_resume"

    def post(self, request):
        data = self.request.POST.dict()
        return JsonResponse(
            [
                ResumeFilter(data, Resume.objects.filter(status=resume_status)).qs.count()
                for resume_status in ResumeStatus
            ], safe=False
        )
