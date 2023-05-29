from django.urls import path

from parsing.views import SuperjobView

app_name = "parsing"

urlpatterns = [
    path('superjob/form', SuperjobView.as_view(), name='superjob-form'),
]
