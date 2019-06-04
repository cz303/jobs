from bot.parser import Parser
from bot.text import Text
from bot.markup import Markup
from telebot.apihelper import ApiException
from .managers import UserManager


__all__ = ['Menu']


class Menu:
    def __init__(self, request, bot):
        self.request = request
        self.bot = bot
        self.parser = Parser(request=self.request)
        self.text = Text()
        self.markup = Markup()
        self.chat_id = self.parser.chat_id()
        self.message_id = self.parser.message_id()
        self.user_id = self.parser.user_id()
        self.username = self.parser.username()
        self.user = UserManager(user_id=self.user_id, username=self.username)

    def send(self):
        text = self.parser.text()

        if text == '/start':
            self.user.create()
            self.start_menu()

        elif text == '🏬 Работодатель':
            self.user.update_profile(profile=1)
            self.employer()

        elif text == '👨‍💻 Работник':
            self.user.update_profile(profile=2)
            self.worker()

        elif text == '📬 Рассказать друзьям':
            self.tell_friends()

        elif text == '🏬 Изменить аккаунт':
            self.start_menu()

        elif text == 'Как мы работаем?':
            self.how_we_are_working(user=self.user)

        elif text == 'Создать вакансию' or \
                text == 'Создать резюме' or \
                text == '◀️ Назад':
            self.send_categories()

        elif text in self.markup.categories:
            self.send_sub_category(category=text)

        elif text in self.markup.get_sub_categories:
            self.create_job()

    def send_message(self, text, reply_markup=None):
        self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def edit_message_text(self, text, reply_markup=None):
        self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def start_menu(self):
        text = self.text.start_menu()
        reply_markup = self.markup.start_menu()
        self.send_message(text=text, reply_markup=reply_markup)

    def employer(self):
        # найти юзера
        text = self.text.employer()
        reply_markup = self.markup.employer()
        self.send_message(text=text, reply_markup=reply_markup)

    def worker(self):
        # add user
        text = self.text.worker()
        reply_markup = self.markup.worker()
        self.send_message(text=text, reply_markup=reply_markup)

    def tell_friends(self):
        text = self.text.tell_friends()
        reply_markup = self.markup.tell_friends()
        self.send_message(text=text, reply_markup=reply_markup)

    def how_we_are_working(self, user):
        text = self.text.how_we_are_working(user)
        self.send_message(text=text)

    def send_categories(self):
        text = self.text.send_categories()
        reply_markup = self.markup.send_categories()
        try:
            self.edit_message_text(text=text, reply_markup=reply_markup)
        except ApiException:
            self.send_message(text=text, reply_markup=reply_markup)

    def send_sub_category(self, category):
        text = self.text.send_sub_category()
        reply_markup = self.markup.send_sub_category(category)
        self.edit_message_text(text=text, reply_markup=reply_markup)

    def create_job(self):
        text = self.text.create_job()
        self.edit_message_text(text=text)
