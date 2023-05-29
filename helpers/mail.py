from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from ssl import create_default_context
from typing import Optional, List, Tuple

from django.conf import settings


def send_email(email: str, subject: str, text: str, files_data: Optional[List[Tuple[str, str]]] = None):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.EMAIL_HOST_USER
        message["To"] = email

        message.attach(MIMEText(text, "html"))

        for file_name, file_data in files_data or []:
            part = MIMEApplication(file_data.encode(), Name=file_name)
            part['Content-Disposition'] = f'attachment; filename="{file_name}"'
            message.attach(part)

        with SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=create_default_context()) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email, message.as_string())

    except BaseException as ex:
        print(ex)
