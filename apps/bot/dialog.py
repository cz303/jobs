from .parser import Parser
from .text import Text
from .markup import Markup


class Dialog:
    def __init__(self, request, bot):
        self.request = request
        self.bot = bot
        self.parser = Parser(request=self.request)
        self.text = Text()
        self.markup = Markup()

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

    def start_menu(self):
        chat_id = self.parser.chat_id()
        text = self.text.start_menu()
        reply_markup = self.markup.start_menu()

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def employer(self):
        # найти юзера
        chat_id = self.parser.chat_id()
        text = self.text.employer()
        reply_markup = self.markup.employer()

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def worker(self):
        # add user
        chat_id = self.parser.chat_id()
        text = self.text.worker()
        reply_markup = self.markup.worker()

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def tell_friends(self):
        chat_id = self.parser.chat_id()
        text = self.text.tell_friends()
        reply_markup = self.markup.tell_friends()

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            reply_markup=reply_markup)

    def how_we_are_working(self):
        # get user
        chat_id = self.parser.chat_id()
        text = self.text.how_we_are_working()

        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML')
