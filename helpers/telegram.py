from logging import getLogger
from typing import Optional, List, Tuple

from asgiref.sync import async_to_sync
from django.conf import settings
from markdownify import markdownify
from telegram import Bot
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

logger = getLogger(__name__)
telegram_bot = Bot(settings.TELEGRAM_BOT_TOKEN)


@async_to_sync
async def send_telegram(telegram_id: int | str, message: str, files_data: Optional[List[Tuple[str, str]]] = None):
    try:
        await telegram_bot.send_message(telegram_id, escape_markdown(markdownify(message)), ParseMode.MARKDOWN)
        for file_name, file_data in files_data or []:
            await telegram_bot.send_document(telegram_id, file_data.encode(), filename=file_name)

    except BaseException as ex:
        print(ex)
