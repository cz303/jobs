from telebot import TeleBot
from django.conf import settings
from helpers.singleton import MetaSingleton


class SetWebHook(metaclass=MetaSingleton):
    def __init__(self):
        self.delete_hook()
        self.set_hook()

    @property
    def bot(self):
        return TeleBot(settings.TOKEN)

    def delete_hook(self):
        self.bot.delete_webhook()

    def set_hook(self):
        self.bot.set_webhook(
            url=f"{settings.DOMAIN}/"
                f"{settings.TOKEN}")
