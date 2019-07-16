from telebot import TeleBot
from django.conf import settings
from helpers.singleton import MetaSingleton
from helpers.logger import logger as log


class SetWebHook(metaclass=MetaSingleton):
    def __init__(self):
        self.bot = TeleBot(settings.TOKEN)
        log.info('delete webhook')
        self.bot.delete_webhook()
        log.info('set webhook')
        self.bot.set_webhook(
            url=f"{settings.DOMAIN}/"
                f"{settings.TOKEN}")
        log.info('setup webhook complete')
