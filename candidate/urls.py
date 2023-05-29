from django.urls import path

from candidate.views import CandidateIndexView, CandidateVacancyDetailView, CandidateProfileView, \
    WorkExperienceUpdateView, WorkExperienceDeleteView, WorkExperienceCreateView, EducationCreateView, \
    EducationUpdateView, EducationDeleteView, ContactCreateView, ContactUpdateView, ContactDeleteView, \
    CandidateVacancyRequestView, CandidateResumeView

app_name = "candidate"

urlpatterns = [
    path('', CandidateIndexView.as_view(), name='candidate-index'),
    path('<int:pk>', CandidateVacancyDetailView.as_view(), name='candidate-vacancy'),
    path('<int:pk>/request', CandidateVacancyRequestView.as_view(), name='candidate-request'),

    path('profile', CandidateProfileView.as_view(), name='candidate-profile'),

    path('profile/resume/<int:pk>', CandidateResumeView.as_view(), name='candidate-resume'),

    path('profile/work_experience/create', WorkExperienceCreateView.as_view(), name='work_experience-create'),
    path('profile/work_experience/<int:pk>/update', WorkExperienceUpdateView.as_view(), name='work_experience-update'),
    path('profile/work_experience/<int:pk>/delete', WorkExperienceDeleteView.as_view(), name='work_experience-delete'),

    path('profile/education/create', EducationCreateView.as_view(), name='education-create'),
    path('profile/education/<int:pk>/update', EducationUpdateView.as_view(), name='education-update'),
    path('profile/education/<int:pk>/delete', EducationDeleteView.as_view(), name='education-delete'),

    path('profile/contact/create', ContactCreateView.as_view(), name='contact-create'),
    path('profile/contact/<int:pk>/update', ContactUpdateView.as_view(), name='contact-update'),
    path('profile/contact/<int:pk>/delete', ContactDeleteView.as_view(), name='contact-delete'),
]
