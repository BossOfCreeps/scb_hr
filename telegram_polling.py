import os

import django
from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update, User
from telegram.ext import ApplicationBuilder, CommandHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scb_hr.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


@sync_to_async
def save_tg_user(tg_user: User):
    from account.models import TelegramUser

    TelegramUser.objects.get_or_create(tg_id=tg_user.id, username=tg_user.username.lower())
    print(f"Add user {tg_user}")


async def start(update: Update, _):
    await save_tg_user(update.effective_user)
    await update.message.reply_text("OK")


app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
print("Запущен бот https://t.me/scb_hack_bot")
app.run_polling()
