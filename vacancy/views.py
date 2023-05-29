from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from vacancy.filters import VacancyFilter
from vacancy.forms import VacancyForm, VacancyCheckForm
from vacancy.models import Vacancy, VacancyCheck


class VacancyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vacancy
    permission_required = "vacancy.change_vacancy"

    def get_context_data(self, **kwargs):
        return {
            "vacancies": VacancyFilter(self.request.GET, Vacancy.objects.all()).qs,
            "filter": VacancyFilter(self.request.GET),
            "show_filter": set(self.request.GET.dict().values()) not in [{""}, set()],
        }


class VacancyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = VacancyForm
    template_name = "vacancy/vacancy_form.html"
    permission_required = "vacancy.change_vacancy"


class VacancyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Vacancy
    permission_required = "vacancy.change_vacancy"

    def get_context_data(self, **kwargs):
        return {
            "vacancy_form": VacancyForm(instance=self.get_object()),
            "check_forms": [VacancyCheckForm(instance=c) for c in self.get_object().checks.all()],
            "create_check_form": VacancyCheckForm,
        }


class VacancyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Vacancy
    fields = "__all__"
    permission_required = "vacancy.change_vacancy"


class VacancyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Vacancy
    permission_required = "vacancy.change_vacancy"

    def get_success_url(self):
        return reverse('vacancy:vacancy-list')


class VacancyCheckCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VacancyCheck
    fields = "__all__"
    permission_required = "vacancy.change_vacancy"


class VacancyCheckUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = VacancyCheck
    fields = "__all__"
    permission_required = "vacancy.change_vacancy"


class VacancyCheckDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = VacancyCheck
    permission_required = "vacancy.change_vacancy"

    def get_success_url(self):
        return reverse('vacancy:vacancy-detail', kwargs={'pk': self.get_object().vacancy_id})
