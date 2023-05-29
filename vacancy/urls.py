from django.urls import path

from vacancy.views import VacancyListView, VacancyDetailView, VacancyUpdateView, VacancyCheckUpdateView, \
    VacancyDeleteView, VacancyCheckDeleteView, VacancyCheckCreateView, VacancyCreateView

app_name = "vacancy"

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy-list'),
    path('<int:pk>', VacancyDetailView.as_view(), name='vacancy-detail'),
    path('create', VacancyCreateView.as_view(), name='vacancy-create'),
    path('<int:pk>/update', VacancyUpdateView.as_view(), name='vacancy-update'),
    path('<int:pk>/delete', VacancyDeleteView.as_view(), name='vacancy-delete'),
    path('checks/create', VacancyCheckCreateView.as_view(), name='check-create'),
    path('checks/<int:pk>/update', VacancyCheckUpdateView.as_view(), name='check-update'),
    path('checks/<int:pk>/delete', VacancyCheckDeleteView.as_view(), name='check-delete'),
]
