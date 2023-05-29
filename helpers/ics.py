from datetime import datetime, timedelta
from typing import List, Optional

from icalendar import Calendar, Event


def create_ics(
        summary: str, start_date: datetime, end_date: datetime, description: str, emails: Optional[List[str]] = None
) -> bytes:
    cal = Calendar()

    for email in emails or []:
        cal.add('attendee', f'MAILTO:{email}')

    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start_date)
    event.add('dtend', end_date)
    event.add('description', description)

    cal.add_component(event)

    return cal.to_ical()


if __name__ == "__main__":
    create_ics(
        "Название",
        datetime.today(),
        datetime.today() + timedelta(hours=1),
        "Описание\nhttps://github.com/",
        ["seva-ra4is@mail.ru"]
    )
