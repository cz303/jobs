from bot.parser import Parser
from bot.text import Text
from bot.markup import Markup

__all__ = ['Menu']


class Menu:
    def __init__(self, request, bot):
        self.request = request
        self.bot = bot
        self.parser = Parser(request=self.request)
        self.text = Text()
        self.markup = Markup()
        self.chat_id = self.parser.chat_id()

    def send(self):
        text = self.parser.text()

        if text == '/start':
            self.start_menu()

        elif text == '🏬 Работодатель':
            self.employer()

        elif text == '👨‍💻 Работник':
            self.worker()

        elif text == '📬 Рассказать друзьям':
            self.tell_friends()

        elif text == '🏬 Изменить аккаунт':
            self.start_menu()

        elif text == '‍Как мы работаем?':
            self.how_we_are_working()

        elif text == 'Создать вакансию':
            self.create_job()

    def send_message(self, text, reply_markup=None):
        self.bot.send_message(
            chat_id=self.chat_id,
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

    def how_we_are_working(self):
        # get user
        text = self.text.how_we_are_working()
        self.send_message(text=text)

    def create_job(self):
        text = self.text.create_job()
        reply_markup = self.markup.create_job()
        self.send_message(text=text, reply_markup=reply_markup)
