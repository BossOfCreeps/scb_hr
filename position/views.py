from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from position.forms import PositionForm
from position.models import Position


class PositionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Position
    permission_required = "position.change_position"


class PositionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Position
    form_class = PositionForm
    permission_required = "position.change_position"


class PositionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Position
    permission_required = "position.change_position"

    def get_success_url(self):
        return reverse('position:position-list')


class PositionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm
    permission_required = "position.change_position"
