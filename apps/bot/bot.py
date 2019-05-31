from telebot import TeleBot
from django.conf import settings
from helpers.singleton import MetaSingleton


class Bot(metaclass=MetaSingleton):
    def __init__(self):
        self.setting = settings
        self.bot = TeleBot(self.setting.TOKEN)
        self.bot.delete_webhook()
        self.bot.set_webhook(url=f"{settings.DOMAIN}/{settings.TOKEN}")
