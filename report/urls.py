from django.urls import path

from report.views import ResumePerVacancyReportView, ResumePerDatetimeReportView, ResumePerVacancyReportAjaxView, \
    ResumePerDatetimeReportAjaxView, ResumeStatusPieReportView, ResumeStatusPieReportAjaxView

app_name = "report"

urlpatterns = [
    path('resume_per_vacancy', ResumePerVacancyReportView.as_view(), name='resume_per_vacancy'),
    path('resume_per_vacancy/ajax', ResumePerVacancyReportAjaxView.as_view(), name='resume_per_vacancy-ajax'),
    path('resume_per_datetime', ResumePerDatetimeReportView.as_view(), name='resume_per_datetime'),
    path('resume_per_datetime/ajax', ResumePerDatetimeReportAjaxView.as_view(), name='resume_per_datetime-ajax'),
    path('resume_status_pie', ResumeStatusPieReportView.as_view(), name='resume_status_pie'),
    path('resume_status_pie/ajax', ResumeStatusPieReportAjaxView.as_view(), name='resume_status_pie-ajax'),
]
