from io import BytesIO
from typing import List

from django.conf import settings
from xlsxwriter import Workbook

from inspector.models import Resume


def create_resumes_xlsx(resumes: List[Resume]) -> bytes:
    output = BytesIO()
    workbook = Workbook(output, options={"remove_timezone": True})
    worksheet = workbook.add_worksheet()

    head = ["ID", "Должность", "Организация", "ФИО", "Статус", "Создан"]
    for i, t in enumerate(head):
        worksheet.write(0, i, t)

    for i, resume in enumerate(resumes, start=1):
        worksheet.write_url(f"A{i + 1}", f"{settings.BASE_URL}/archive/{resume.id}", string=f"{resume.id}")
        worksheet.write(i, 1, resume.vacancy.position.name)
        worksheet.write(i, 2, resume.vacancy.position.organisation.name)
        worksheet.write(i, 3, resume.candidate.full_name)
        worksheet.write(i, 4, resume.get_status_display())
        worksheet.write(i, 5, resume.created, workbook.add_format({"num_format": "yy/mm/dd hh:mm"}))

    workbook.close()
    output.seek(0)
    return output.getvalue()
