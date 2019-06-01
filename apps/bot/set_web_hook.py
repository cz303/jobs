from telebot import TeleBot
from django.conf import settings


class SetWebHook():
    def __init__(self):
        self.bot = TeleBot(settings.TOKEN)
        self.bot.delete_webhook()

        self.bot.set_webhook(
            url=f"{settings.DOMAIN}/"
                f"{settings.TOKEN}")
