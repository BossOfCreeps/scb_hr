from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType

from account.models import EmailValidation, TelegramUser

admin.site.register(EmailValidation)
admin.site.register(TelegramUser)

admin.site.register(Permission)
admin.site.register(ContentType)
