from __future__ import absolute_import

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scb_hr.settings')

from datetime import timedelta

from celery import Celery
from django.utils.timezone import now

from helpers.mail import send_email
from helpers.telegram import send_telegram

app = Celery('scb_hr')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def send_out_interview_reminders():
    from inspector.models import Interview

    for interview in Interview.objects.filter(start_date__lte=now() + timedelta(days=1)):
        interview.send_reminder_messages()


@app.task()
def async_send_email(*args, **kwargs):
    send_email(*args, **kwargs)


@app.task()
def async_send_telegram(*args, **kwargs):
    send_telegram(*args, **kwargs)
