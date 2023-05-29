from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView

from inspector.constants import ResumeStatus
from inspector.filters import ResumeFilter
from inspector.forms import VacancyApproveForm, InterviewForm, VacancyDenyForm
from inspector.models import Resume, Interview


class ResumeListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'inspector/resume_list.html'
    permission_required = "inspector.change_resume"

    def get_context_data(self, **kwargs):
        return {
            "resumes": [
                r
                for r in ResumeFilter(self.request.GET, Resume.objects.filter(status=ResumeStatus.NEW)).qs
                if r.check_permission(self.request.user)
            ],
            "filter": ResumeFilter(self.request.GET),
            "show_filter": set(self.request.GET.dict().values()) not in [{""}, set()],
            "interview_form": InterviewForm(),
        }


class ResumeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Resume
    permission_required = "inspector.change_resume"

    def get_context_data(self, **kwargs):
        return {
            "resume": self.get_object(),
            "interview_form": InterviewForm()
        }


class ResumeApproveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.change_resume"

    def post(self, request):
        f = VacancyApproveForm(self.request.POST)
        if f.is_valid():
            Resume.objects.get(pk=f.cleaned_data["resume"]).approve(self.request.user, f.cleaned_data["approve_text"])
            return redirect('inspector:resume-list')


class ResumeDenyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "inspector.change_resume"

    def post(self, request):
        f = VacancyDenyForm(self.request.POST)
        if f.is_valid():
            Resume.objects.get(pk=f.cleaned_data["resume"]).deny(self.request.user, f.cleaned_data["deny_text"])
            return redirect('inspector:resume-list')


class InterviewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Interview
    fields = "__all__"
    permission_required = "inspector.add_interview"

    def form_valid(self, form):
        result = super(InterviewCreateView, self).form_valid(form)
        form.instance.send_creation_messages()
        return result
