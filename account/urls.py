from django.urls import path, include

from account.views import RegistrationView, EmailValidationCreateView, EmailValidationApproveView, ProfileUpdateView

app_name = "account"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('registration', RegistrationView.as_view(), name='registration'),
    path('update', ProfileUpdateView.as_view(), name='update'),
    path('valid_email/create', EmailValidationCreateView.as_view(), name='valid_email-create'),
    path('valid_email/approve', EmailValidationApproveView.as_view(), name='valid_email-approve'),
]
