from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, UpdateView

from account.models import CustomUser, EmailValidation
from helpers import random_code
from scb_hr.celery import async_send_email


class RegistrationView(CreateView):
    model = CustomUser
    fields = ["email", "password", "last_name", "first_name", "middle_name", "image"]

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        result = super(RegistrationView, self).form_valid(form)
        login(self.request, form.instance)
        return result


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["last_name", "first_name", "middle_name", "image"]

    def get_object(self, queryset=None):
        return self.request.user


class EmailValidationCreateView(View):
    def post(self, request):
        obj = EmailValidation.objects.create(email=self.request.POST["email"], value=random_code())
        async_send_email.delay(obj.email, "Код авторизации", f"Код авторизации на портале: {obj.value}")
        return HttpResponse()


class EmailValidationApproveView(View):
    def post(self, request):
        obj = EmailValidation.objects.filter(email=self.request.POST["email"], value=self.request.POST["value"]).first()
        if obj:
            obj.delete()
            return HttpResponse()

        return HttpResponse(status=400)
