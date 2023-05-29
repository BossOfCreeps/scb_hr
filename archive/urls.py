from django.urls import path

from archive.views import ArchiveListView, ArchiveDetailView, ArchiveDownload

app_name = "archive"

urlpatterns = [
    path('', ArchiveListView.as_view(), name='archive-list'),
    path('download', ArchiveDownload.as_view(), name='archive-download'),
    path('<int:pk>', ArchiveDetailView.as_view(), name='archive-detail'),
]
