import time
from bot.business_logic.parser import Parser
from bot.business_logic.text import Text
from bot.business_logic.markup import Markup
from telebot.apihelper import ApiException
from bot.models.user_manager import UserManager
from bot.models.job_manager import JobManager
from bot.models.resume_manager import ResumeManager
from bot.models.dialog_job_manager import DialogJobManager
from bot.models.dialog_resume_manager import DialogResumeManager

__all__ = ('Menu',)


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

    @property
    def command_maps(self):
        return {
            '/start': self.start_menu,
            '🏬 Работодатель': self.employer,
            '👨‍💻 Работник': self.worker,
            '📬 Рассказать друзьям': self.tell_friends,
            '🏬 Изменить аккаунт': self.start_menu,
            'Как мы работаем?': self.how_we_are_working,
            'Мои резюме': self.my_resume,
            'Мои вакансии': self.my_vacations,
            'Создать вакансию': self.send_categories,
            'Создать резюме': self.send_categories,
            '◀️ Назад': self.send_categories,
        }

    def send(self):
        text = self.parser.text()
        user = self.user.get_user()

        if not user:
            return self.start_menu()

        command = self.command_maps.get(text, None)

        if command:
            try:
                return command()
            except TypeError:
                return command(user=user)

        if text in self.markup.categories:
            self.send_sub_category(category=text, user=user)

        # TODO: create job

        elif text in self.markup.get_sub_categories and user.profile == 1:
            self.looking_for(position=text, user=user)

        # TODO: First step

        elif self.check_looking_for():
            self.wage(text=text, user=user)

        # TODO: create resume

        # elif text in self.markup.get_sub_categories and user.profile == 2:
        #     self.name(position=text, user=user)

        # elif self.check_name():
        #     self.age(text=text)
        # elif self.check_wage():
        #     self.city(text=text)
        # elif self.check_age():
        #     self.work_city(text=text)
        # elif self.check_city():
        #     self.experience(text=text)
        # elif self.check_work_city():
        #     self.lang(text=text)
        # elif self.check_lang():
        #     self.work_experience(text=text)
        # elif self.check_work_experience():
        #     self.education(text=text)
        # elif self.check_education():
        #     self.work_description(text=text)
        # elif self.check_work_description():
        #     self.work_moderation()
        # elif self.check_experience():
        #     self.description(text=text)
        # elif self.check_description():
        #     self.write_to_employer(text=text)
        # elif text == 'Где искать username?':
        #     self.where_to_find_username_link()
        # elif self.check_write_to_employer():
        #     self.moderation()

    def my_vacations(self):
        user = self.user.get_user()
        if user and user.profile == 1:
            vacations = JobManager(user_id=user.id).get_vacations()
            if vacations:
                text = ''
                markup = ''
                if text and markup:
                    self.send_message(text=text, reply_markup=markup)
                else:
                    text = ''
                    self.send_message(text=text)

    def my_resume(self):
        user = self.user.get_user()
        if user and user.profile == 2:
            resumes = ResumeManager(user_id=user.id).get_resume()
            if resumes:
                text = self.text.my_resume()
                markup = self.markup.my_resume(resumes=resumes)
                # if text and markup:
                self.send_message(text=text, reply_markup=markup)
            else:
                text = self.text.my_resume_on_moderation()
                self.send_message(text=text)

    def work_city(self, text):
        user = self.user.get_user()
        if user and user.profile == 2:
            ResumeManager(user_id=user.id).update_city(city=text)
            DialogResumeManager(user_id=user.id).city()
            text = self.text.work_city()
            self.send_message(text=text)

    def check_work_city(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_city()

    def work_moderation(self):
        user = self.user.get_user()
        if user:
            DialogResumeManager(user_id=user.id).clean()
        text = self.text.work_moderation()
        self.send_message(text=text)

    def check_work_description(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_description()

    def work_description(self, text):
        user = self.user.get_user()
        if user:
            ResumeManager(user_id=user.id).update_description(description=text)
            DialogResumeManager(user_id=user.id).description()
            text = self.text.work_description()
            self.send_message(text=text)

    def check_education(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_education()

    def work_experience(self, text):
        user = self.user.get_user()
        if user and user.profile == 2:
            ResumeManager(user_id=user.id).update_experience(experience=text)
            DialogResumeManager(user_id=user.id).experience()
            text = self.text.work_experience()
            self.send_message(text=text)

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

    def check_name(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_name()

    def check_age(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_age()

    def check_lang(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_lang()

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

    def check_work_experience(self):
        user = self.user.get_user()
        if user:
            return DialogResumeManager(user_id=user.id).check_experience()

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

    def send_categories(self, user):
        if user.profile == 1:
            JobManager(user_id=user.id).clean()
            dialog = DialogJobManager(user_id=user.id)
            dialog.clean()
            dialog.create()
        else:
            ResumeManager(user_id=user.id).clean()
            dialog = DialogResumeManager(user_id=user.id)
            dialog.clean()
            dialog.create()

        text = self.text.send_categories()
        reply_markup = self.markup.send_categories()

        try:
            self.edit_message_text(text=text, reply_markup=reply_markup)
        except ApiException:
            self.send_message(text=text, reply_markup=reply_markup)

    def send_sub_category(self, category, user):
        if user.profile == 1:
            JobManager(user_id=user.id).create(category=category)
            DialogJobManager(user_id=user.id).update_category()
        else:
            ResumeManager(user_id=user.id).create(category=category)
            DialogResumeManager(user_id=user.id).update_category()

        text = self.text.send_sub_category()
        reply_markup = self.markup.send_sub_category(category)

        self.edit_message_text(text=text, reply_markup=reply_markup)

    def looking_for(self, position, user):
        JobManager(user_id=user.id).update_position(position=position)
        DialogJobManager(user_id=user.id).looking_for()
        text = self.text.looking_for()
        self.send_message(text=text)

    def name(self, position, user):
        ResumeManager(user_id=user.id).update_position(position=position)
        DialogResumeManager(user_id=user.id).name()
        text = self.text.name()
        self.send_message(text=text)

    def wage(self, text, user):
        JobManager(user_id=user.id).update_looking_for(looking_for=text)
        DialogJobManager(user_id=user.id).wage()
        text = self.text.wage()
        self.send_message(text=text)

    def age(self, text):
        user = self.user.get_user()
        if user:
            ResumeManager(user_id=user.id).update_name(name=text)
            DialogResumeManager(user_id=user.id).age()
            text = self.text.age()
            self.send_message(text=text)

    def city(self, text):
        user = self.user.get_user()
        if user and user.profile == 1:
            JobManager(user_id=user.id).update_city(city=text)
            DialogJobManager(user_id=user.id).city()
            text = self.text.city()
            self.send_message(text=text)

    def lang(self, text):
        user = self.user.get_user()
        if user:
            ResumeManager(user_id=user.id).update_lang(lang=text)
            DialogResumeManager(user_id=user.id).lang()
            text = self.text.lang()
            self.send_message(text=text)

    def education(self, text):
        user = self.user.get_user()
        if user:
            ResumeManager(user_id=user.id).update_education(education=text)
            DialogResumeManager(user_id=user.id).education()
            text = self.text.education()
            self.send_message(text=text)

    def experience(self, text):
        user = self.user.get_user()
        if user and user.profile == 1:
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
