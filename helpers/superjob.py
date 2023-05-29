from pprint import pprint
from typing import Optional, List, Tuple

import requests
from django.conf import settings


def parse_super_job(
        text: Optional[str] = None, town: Optional[str] = None, count: Optional[int] = None, page: Optional[int] = None
) -> Tuple[int, List[dict]]:
    """
    https://api.superjob.ru/client/#resumes

    :param page:
    :param count:
    :param text:
    :param town:
    :return:
    """

    if text is None:
        return 0, []

    town_id = None
    if town:
        town_id = requests.get(
            "https://api.superjob.ru/2.0/towns/",
            headers={"X-Api-App-Id": settings.SUPERJOB_TOKEN},
            params={"keyword": town}
        ).json()["objects"][0]["id"]

    response = requests.get(
        "https://api.superjob.ru/2.0/resumes/",
        headers={"X-Api-App-Id": settings.SUPERJOB_TOKEN},
        params={
            "keyword": text,
            "t": [town_id],
            "count": count,
            "page": (page - 1) if page is not None else 0,
        }
    )

    pprint(response.json()["objects"][0])

    results = []
    for obj in response.json()["objects"]:
        results.append(
            {
                "position": obj["profession"],
                "age": obj.get("age"),
                "gender": obj["gender"]["title"],
                "url": obj["link"],
                "description": obj["achievements"],
                "town": obj["town"]["genitive"],
                "payment": obj["payment"],
                "experience_text": obj["experience_text"],
                "work_history": [
                    {
                        "company": work_history["name"],
                        "position": work_history["profession"],
                        "description": work_history["work"],
                    }
                    for work_history in obj["work_history"]
                ]
            }
        )

    return response.json()["total"], results
