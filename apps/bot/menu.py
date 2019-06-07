from bot.parser import Parser
from bot.text import Text
from bot.markup import Markup
from telebot.apihelper import ApiException
from .user_manager import UserManager
from .job_manager import JobManager
from .dialog_job_manager import DialogJobManager
import time

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
            self.start_menu()
        elif text == '🏬 Работодатель':
            self.employer()
        elif text == '👨‍💻 Работник':
            self.worker()
        elif text == '📬 Рассказать друзьям':
            self.tell_friends()
        elif text == '🏬 Изменить аккаунт':
            self.start_menu()
        elif text == 'Как мы работаем?':
            self.how_we_are_working()
        elif text == 'Создать вакансию' or \
                text == 'Создать резюме' or \
                text == '◀️ Назад':
            self.send_categories()
        elif text in self.markup.categories:
            self.send_sub_category(category=text)
        elif text in self.markup.get_sub_categories:
            self.looking_for(position=text)
        elif self.check_looking_for():
            self.wage(text=text)
        elif self.check_wage():
            self.city(text=text)
        elif self.check_city():
            self.experience(text=text)
        elif self.check_experience():
            self.description(text=text)
        elif self.check_description():
            self.write_to_employer(text=text)
        elif text == 'Где искать username?':
            self.where_to_find_username_link()
        elif self.check_write_to_employer():
            self.moderation()

    def moderation(self):
        user = self.user.get_user()
        if user:
            DialogJobManager(user_id=user.id).clean()
        text = self.text.moderation()
        self.send_message(text=text)

    def where_to_find_username_link(self):
        text = self.text.where_to_find_username_link()
        self.send_message(text=text)
        time.sleep(3.0)
        self.where_to_find_username()

    def where_to_find_username(self):
        text = self.text.where_to_find_username()
        self.send_message(text=text)

    def check_looking_for(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_looking_for()

    def check_wage(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_wage()

    def check_city(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_city()

    def check_experience(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_experience()

    def check_description(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_description()

    def check_write_to_employer(self):
        user = self.user.get_user()
        if user:
            return DialogJobManager(user_id=user.id).check_write_to_employer()

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
        self.user.create()
        text = self.text.start_menu()
        reply_markup = self.markup.start_menu()
        self.send_message(text=text, reply_markup=reply_markup)

    def employer(self):
        self.user.update_profile(profile=1)
        text = self.text.employer()
        reply_markup = self.markup.employer()
        self.send_message(text=text, reply_markup=reply_markup)

    def worker(self):
        self.user.update_profile(profile=2)
        text = self.text.worker()
        reply_markup = self.markup.worker()
        self.send_message(text=text, reply_markup=reply_markup)

    def tell_friends(self):
        text = self.text.tell_friends()
        reply_markup = self.markup.tell_friends()
        self.send_message(text=text, reply_markup=reply_markup)

    def how_we_are_working(self):
        user = self.user.get_user()
        text = self.text.how_we_are_working(profile=user.profile)
        self.send_message(text=text)

    def send_categories(self):
        text = self.text.send_categories()
        reply_markup = self.markup.send_categories()
        try:
            self.edit_message_text(text=text, reply_markup=reply_markup)
        except ApiException:
            self.send_message(text=text, reply_markup=reply_markup)

    def send_sub_category(self, category):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).create(category=category)
            text = self.text.send_sub_category()
            reply_markup = self.markup.send_sub_category(category)
            self.edit_message_text(text=text, reply_markup=reply_markup)

    def looking_for(self, position):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_position(position=position)
            DialogJobManager(user_id=user.id).clean()
            DialogJobManager(user_id=user.id).create()
            text = self.text.looking_for()
            self.send_message(text=text)

    def wage(self, text):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_wage(wage=text)
            DialogJobManager(user_id=user.id).wage()
            text = self.text.wage()
            self.send_message(text=text)

    def city(self, text):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_city(city=text)
            DialogJobManager(user_id=user.id).city()
            text = self.text.city()
            self.send_message(text=text)

    def experience(self, text):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_experience(experience=text)
            DialogJobManager(user_id=user.id).experience()
            text = self.text.experience()
            self.send_message(text=text)

    def description(self, text):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_description(description=text)
            DialogJobManager(user_id=user.id).description()
            text = self.text.description()
            self.send_message(text=text)

    def write_to_employer(self, text):
        user = self.user.get_user()
        if user:
            JobManager(user_id=user.id).update_write_to_employer(
                write_to_employer=text)
            DialogJobManager(user_id=user.id).write_to_employer()
            text = self.text.write_to_employer()
            reply_markup = self.markup.write_to_employer()
            self.send_message(text=text, reply_markup=reply_markup)
