from django.urls import path

from inspector.views import ResumeListView, ResumeDetailView, ResumeApproveView, ResumeDenyView, InterviewCreateView

app_name = "inspector"

urlpatterns = [
    path('', ResumeListView.as_view(), name='resume-list'),
    path('<int:pk>', ResumeDetailView.as_view(), name='resume-detail'),
    path('approve', ResumeApproveView.as_view(), name='resume-approve'),
    path('deny', ResumeDenyView.as_view(), name='resume-deny'),

    path('interview/create', InterviewCreateView.as_view(), name='interview-create'),
]
