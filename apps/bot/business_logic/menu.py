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
            'r:return': self.my_resume,
            'v:return': self.my_vacations,
            'Мои вакансии': self.my_vacations,
            'Создать вакансию': self.send_categories,
            'Создать резюме': self.send_categories,
            '◀️ Назад': self.send_categories,
            'Где искать username?': self.where_to_find_username_link,
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

        if user.profile == 1:

            if text in self.markup.get_sub_categories:
                self.looking_for(position=text, user=user)

            # First step

            elif self.check_looking_for(user=user):
                self.wage(text=text, user=user)

            # Second step

            elif self.check_wage(user=user):
                self.city(text=text, user=user)

            # Three step

            elif self.check_city(user=user):
                self.experience(text=text, user=user)

            # Four step

            elif self.check_experience(user=user):
                self.description(text=text, user=user)

            # Five step

            elif self.check_description(user=user):
                self.write_to_employer(text=text, user=user)

            # Six step final create job send to moderation

            elif self.check_write_to_employer(user=user):
                self.moderation(text=text, user=user)

        # TODO: create resume

        elif user.profile == 2:

            if text in self.markup.get_sub_categories:
                self.name(position=text, user=user)

            # First step

            elif self.check_name(user=user):
                self.age(text=text, user=user)

            # Second step

            elif self.check_age(user=user):
                self.work_city(text=text, user=user)

            # Three step

            elif self.check_work_city(user=user):
                self.lang(text=text, user=user)

            # Four step

            elif self.check_lang(user=user):
                self.work_experience(text=text, user=user)

            # Five step

            elif self.check_work_experience(user=user):
                self.education(text=text, user=user)

            # Six step

            elif self.check_education(user=user):
                self.work_description(text=text, user=user)

            # Seven step final create resume

            elif self.check_work_description(user=user):
                self.work_moderation(text=text, user=user)

        # TODO: Update or delete vacations

        if 'vacations' in text:
            self.view_vacations(user=user, text=text)

        elif 'v:update' in text:
            self.update_vacations(user=user, text=text)

        elif 'v:del' in text:
            self.delete_vacations(user=user, text=text)

        # TODO: Update or delete resumes

        if 'resumes' in text:
            self.view_resume(user=user, text=text)

        elif 'r:update' in text:
            self.update_resume(user=user, text=text)

        elif 'r:del' in text:
            self.delete_resume(user=user, text=text)

        # TODO: Search resume

    def delete_resume(self, user, text):
        resume_id = text.split(':')[-1]
        ResumeManager(user_id=user.id).delete_resume(resume_id=resume_id)
        self.my_resume(user=user)

    def update_resume(self, user, text):
        resume_id = text.split(':')[-1]
        ResumeManager(user_id=user.id).update_resume(resume_id=resume_id)
        self.view_resume(user=user, text=text)

    def view_resume(self, user, text):
        resume_id = text.split(':')[-1]
        resume = ResumeManager(
            user_id=user.id).get_resume_for_id(resume_id=resume_id)
        text = self.text.view_resume(resume=resume)
        markup = self.markup.view_resume(resume=resume)
        self.edit_message_text(text=text, reply_markup=markup)

    def delete_vacations(self, user, text):
        vacation_id = text.split(':')[-1]
        JobManager(user_id=user.id).delete_vacations(vacation_id=vacation_id)
        self.my_vacations(user=user)

    def update_vacations(self, user, text):
        vacation_id = text.split(':')[-1]
        JobManager(user_id=user.id).update_vacations(vacation_id=vacation_id)
        self.view_vacations(user=user, text=text)

    def view_vacations(self, user, text):
        vacation_id = text.split(':')[-1]
        vacancy = JobManager(
            user_id=user.id).get_vacation_for_id(vacation_id=vacation_id)
        text = self.text.view_vacations(vacancy=vacancy)
        markup = self.markup.view_vacations(vacancy=vacancy)
        self.edit_message_text(text=text, reply_markup=markup)

    def my_vacations(self, user):
        vacations = JobManager(user_id=user.id).get_vacations()

        if vacations:
            text = self.text.my_vacations()
            markup = self.markup.my_vacations(vacations=vacations)

            if text and markup.keyboard:
                self.send_message(text=text, reply_markup=markup)
            else:
                text = self.text.my_vacation_on_moderation()
                self.send_message(text=text)
        else:
            text = self.text.my_vacation_on_moderation()
            self.send_message(text=text)

    def my_resume(self, user):
        resumes = ResumeManager(user_id=user.id).get_resume()
        if resumes:
            text = self.text.my_resume()
            markup = self.markup.my_resume(resumes=resumes)

            if text and markup.keyboard:
                self.send_message(text=text, reply_markup=markup)
            else:
                text = self.text.my_resume_on_moderation()
                self.send_message(text=text)
        else:
            text = self.text.my_resume_on_moderation()
            self.send_message(text=text)

    def work_city(self, text, user):
        ResumeManager(user_id=user.id).update_age(age=text)
        DialogResumeManager(user_id=user.id).city()
        text = self.text.work_city()
        self.send_message(text=text)

    def check_work_city(self, user):
        return DialogResumeManager(user_id=user.id).check_city()

    def work_moderation(self, text, user):
        ResumeManager(user_id=user.id).update_description(description=text)
        DialogResumeManager(user_id=user.id).clean()
        text = self.text.work_moderation()
        self.send_message(text=text)

    def check_work_description(self, user):
        return DialogResumeManager(user_id=user.id).check_description()

    def work_description(self, text, user):
        ResumeManager(user_id=user.id).update_education(education=text)
        DialogResumeManager(user_id=user.id).description()
        text = self.text.work_description()
        self.send_message(text=text)

    def check_education(self, user):
        return DialogResumeManager(user_id=user.id).check_education()

    def work_experience(self, text, user):
        ResumeManager(user_id=user.id).update_lang(lang=text)
        DialogResumeManager(user_id=user.id).experience()
        text = self.text.work_experience()
        self.send_message(text=text)

    def moderation(self, text, user):
        JobManager(user_id=user.id).update_write_to_employer(
            write_to_employer=text)
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

    def check_looking_for(self, user):
        return DialogJobManager(user_id=user.id).check_looking_for()

    def check_name(self, user):
        return DialogResumeManager(user_id=user.id).check_name()

    def check_age(self, user):
        return DialogResumeManager(user_id=user.id).check_age()

    def check_lang(self, user):
        return DialogResumeManager(user_id=user.id).check_lang()

    def check_wage(self, user):
        return DialogJobManager(user_id=user.id).check_wage()

    def check_city(self, user):
        return DialogJobManager(user_id=user.id).check_city()

    def check_experience(self, user):
        return DialogJobManager(user_id=user.id).check_experience()

    def check_work_experience(self, user):
        return DialogResumeManager(user_id=user.id).check_experience()

    def check_description(self, user):
        return DialogJobManager(user_id=user.id).check_description()

    def check_write_to_employer(self, user):
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

    def age(self, text, user):
        ResumeManager(user_id=user.id).update_name(name=text)
        DialogResumeManager(user_id=user.id).age()
        text = self.text.age()
        self.send_message(text=text)

    def city(self, text, user):
        JobManager(user_id=user.id).update_wage(wage=text)
        DialogJobManager(user_id=user.id).city()
        text = self.text.city()
        self.send_message(text=text)

    def lang(self, text, user):
        ResumeManager(user_id=user.id).update_city(city=text)
        DialogResumeManager(user_id=user.id).lang()
        text = self.text.lang()
        self.send_message(text=text)

    def education(self, text, user):
        ResumeManager(user_id=user.id).update_experience(experience=text)
        DialogResumeManager(user_id=user.id).education()
        text = self.text.education()
        self.send_message(text=text)

    def experience(self, text, user):
        JobManager(user_id=user.id).update_city(city=text)
        DialogJobManager(user_id=user.id).experience()
        text = self.text.experience()
        self.send_message(text=text)

    def description(self, text, user):
        JobManager(user_id=user.id).update_experience(experience=text)
        DialogJobManager(user_id=user.id).description()
        text = self.text.description()
        self.send_message(text=text)

    def write_to_employer(self, text, user):
        JobManager(user_id=user.id).update_description(description=text)
        DialogJobManager(user_id=user.id).write_to_employer()
        text = self.text.write_to_employer()
        reply_markup = self.markup.write_to_employer()
        self.send_message(text=text, reply_markup=reply_markup)
