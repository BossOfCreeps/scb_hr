from django.urls import path

from position.views import PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView

app_name = "position"

urlpatterns = [
    path('', PositionListView.as_view(), name='position-list'),
    path('create', PositionCreateView.as_view(), name='position-create'),
    path('<int:pk>', PositionUpdateView.as_view(), name='position-update'),
    path('<int:pk>/delete', PositionDeleteView.as_view(), name='position-delete'),
]
