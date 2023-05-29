from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, CreateView

from candidate.forms import WorkExperienceForm, EducationForm, ContactForm, CandidateVacancyRequestForm
from candidate.models import WorkExperience, Education, Contact
from inspector.models import ResumeFile, Resume
from vacancy.filters import VacancyFilter
from vacancy.models import Vacancy


class CandidateIndexView(TemplateView):
    template_name = "candidate/index.html"

    def get_context_data(self, **kwargs):
        return {
            "vacancies": VacancyFilter(self.request.GET, Vacancy.objects.all()).qs,
            "filter": VacancyFilter(self.request.GET),
            "show_filter": set(self.request.GET.dict().values()) not in [{""}, set()],
        }


class CandidateVacancyDetailView(DetailView):
    model = Vacancy
    template_name = "candidate/vacancy.html"


class CandidateVacancyRequestView(LoginRequiredMixin, CreateView):
    form_class = CandidateVacancyRequestForm
    template_name = "candidate/vacancy_request.html"

    def get_context_data(self, **kwargs):
        return {"form": self.form_class(), "vacancy": Vacancy.objects.get(pk=self.kwargs["pk"])}

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        form.instance.vacancy_id = self.kwargs["pk"]
        result = super(CandidateVacancyRequestView, self).form_valid(form)

        for file in form.cleaned_data["files"]:
            ResumeFile.objects.create(resume=form.instance, file=file)

        return result


class CandidateProfileView(LoginRequiredMixin, TemplateView):
    template_name = "candidate/profile.html"


class CandidateResumeView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = "candidate/resume.html"

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
                if vacancy_checks[i].visible_for_candidate
            ],
        }


class WorkExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = "candidate/workexperience_update.html"


class WorkExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkExperience

    def get_success_url(self):
        return reverse('candidate:candidate-profile')


class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = "candidate/workexperience_create.html"

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        return super(WorkExperienceCreateView, self).form_valid(form)


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = "candidate/education_update.html"


class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education

    def get_success_url(self):
        return reverse('candidate:candidate-profile')


class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = "candidate/education_create.html"

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        return super(EducationCreateView, self).form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "candidate/contact_update.html"


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact

    def get_success_url(self):
        return reverse('candidate:candidate-profile')


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "candidate/contact_create.html"

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        return super(ContactCreateView, self).form_valid(form)
