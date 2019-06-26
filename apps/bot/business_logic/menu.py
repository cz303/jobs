import time
from django.conf import settings
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent
from bot.business_logic.parser import Parser
from bot.business_logic.text import Text
from bot.business_logic.markup import Markup
from telebot.apihelper import ApiException
from bot.models.managers.user_manager import UserManager
from bot.models.managers.job_manager import JobManager
from bot.models.managers.resume_manager import ResumeManager
from bot.models.managers.dialog_job_manager import DialogJobManager
from bot.models.managers.dialog_resume_manager import DialogResumeManager
from bot.models.managers.dialog_search_manager import DialogSearchManager
from bot.models.managers.city_manager import city_valid
from bot.models.managers.search_manager import SearchManager
from bot.business_logic.liqpay import LiqPay
# from bot.models.managers.statistics_manager import StatisticsManager
# from bot.models.tables import Statistics


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
        self.callback_query_id = self.parser.callback_id()
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
            'Поиск вакансий': self.search_vacancy,
            '#jobs': self.search_response,
            '✅ Опубликовать': self.publish,
            'Оплатить в: USD(доллар)': self.pay,
        }

    def send(self):
        text = self.parser.text()
        user = self.user.get_user()

        if not user:
            return self.start_menu()

        if isinstance(text, dict):
            return self.my_score(text=text)

        command = self.command_maps.get(text, None)

        if command:
            try:
                return command()
            except TypeError:
                try:
                    return command(user=user)
                except TypeError:
                    return command(user=user, text=text)

        if text in self.markup.categories:
            self.send_sub_category(category=text, user=user)

        if text in self.markup.pay_buttons():
            self.redirect_to_liq(text=text, user=user)

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

            # TODO: Search resume

            # First step

            if self.check_search_start(user=user):
                self.search_city(user=user, text=text)

            # Second step

            elif self.check_search_city(user=user):
                self.search_category(user=user, text=text)

            # Three step

            elif self.check_search_category(user=user):
                self.search_sub_category(user=user, text=text)

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

    def redirect_to_liq(self, text, user):
        amount = text.split()[1]
        liq_pay = LiqPay(settings.PUBLIC_KEY, settings.PRIVATE_KEY)
        res = liq_pay.api(url='request', params={"action": "invoice_bot",
                                                 "version": "3",
                                                 "amount": amount,
                                                 "currency": "USD",
                                                 "order_id": int(time.time()),
                                                 "phone": user.phone})
        if res['status'] == 'error':
            text = self.text.redirect_to_liq_error()
            self.send_message(text=text)

            time.sleep(3)
            self.start_menu()

        elif res['status'] == 'invoice_wait':
            money = text.split()[1]
            value = text.split()[2]
            text = self.text.liq(count=money, value=value)
            markup = self.markup.liq(url=res.get('href'))
            self.send_message(text=text, reply_markup=markup)

    def pay(self):
        text = self.text.pay()
        markup = self.markup.pay()
        self.edit_message_text(text=text, reply_markup=markup)

    def my_score(self, text):
        user = UserManager(user_id=self.user_id)
        user.set_phone(phone=text.get('phone_number'))
        balance = user.get_score()
        text = self.text.my_score(balance)
        markup = self.markup.my_score()
        self.send_message(text=text, reply_markup=markup)

    def send_to(self, resumes, job):
        # рассылка рабочим
        for i in resumes:
            text = self.text.send_resume(job)
            self.send_message(user_id=i.user.user_id, text=text)

    # def money_send(self, user, text):
    #     # цена за рассылку
    #     price = 0.02
    #     # резюме которое будем рассылать
    #     job = JobManager(user_id=user.id).last_job()
    #     # ищем рабочих по заданым критериям
    #     resumes = ResumeManager(user_id=self.user_id).search_resume(
    #         city=job.city,
    #         category=job.category,
    #         posistion=job.position)
    #     # если нет резюме отсылаем отказ
    #     if not resumes:
    #         text = self.text.not_jobs()
    #         return self.send_message(text=text)
    #     else:
    #         # начинаю продвижение вакансии
    #         text = self.text.start_send()
    #         self.send_message(text=text)

            # if float(user.credit) < price:
            #     text = self.text.top_up_account(balance=user.credit)
            #     markup = self.markup.my_score()
            #     return self.edit_message_text(text=text, reply_markup=markup)
            #
            #
            #         # сбор статистики
            #         count = len(resumes)
            #         funds_spent = count * price
            #         sent = [i.user.user_id for i in resumes]
            #         stat = StatisticsManager(user_id=user.id)
            #
            #         try:
            #             free = stat.free_send()
            #         except Statistics.DoesNotExist:
            #             stat.create()
            #             free = stat.free_send()
            #
            #         # перые 10 рассылок
            #         st = stat.get()
            #
            #         if free > 0:
            #             free_send = float(free) - count
            #             text = self.text.statistics(
            #                 count=count,
            #                 price=price,
            #                 funds_spent=funds_spent,
            #                 free_send_count=st.free_send - count,
            #                 free_send=count)
            #             # рассылка рабочим
            #             self.send_to(resumes=resumes, job=job)
            #             self.send_message(text=text)
            #             stat.save(
            #                 count=float(st.count) + float(count),
            #                 sent_to_users=sent,
            #                 price=price,
            #                 funds_spent=float(
            #                     st.funds_spent) + float(funds_spent),
            #                 free_send=free_send)
            #         else:
            #             # считаем баланс
            #             balance = self.user.get_score()
            #             credit = float(balance) - funds_spent
            #
            #             if credit < 1 and credit < len(resumes):
            #                 text = self.text.top_up_account(balance)
            #                 self.send_message(text=text)
            #             else:
            #                 # рассылка рабочим
            #                 self.send_to(resumes=resumes, job=job)
            #                 # обновляем баланс
            #                 self.user.update_credit(credit=credit)
            #                 text = self.text.statistics(
            #                     count=count,
            #                     price=price,
            #                     funds_spent=funds_spent,
            #                     credit=credit
            #                 )
            #                 stat.save(
            #                     count=float(st.count) + float(count),
            #                     sent_to_users=sent,
            #                     price=price,
            #                     funds_spent=float(
            #                         st.funds_spent) + float(funds_spent),
            #                     free_send=0
            #                 )
            #                 self.send_message(text=text)

    def resume_and_job_to_send(self, user, text):
        # резюме которое будем рассылать
        job = JobManager(user_id=user.id).last_job()
        # ищем рабочих по заданым критериям
        resumes = ResumeManager(user_id=self.user_id).search_resume(
            city=job.city,
            category=job.category,
            posistion=job.position)
        return job, resumes

    def free_send(self, user, text):
        pass

    def start_send(self, user, text):
        #  price = 0.02
        time.sleep(5)
        text = self.text.top_up_account(balance=user.credit)
        markup = self.markup.my_score()
        return self.edit_message_text(text=text, reply_markup=markup)

    def publish(self, user):
        text = self.text.publish(user)
        if user.profile == 1:
            JobManager(user_id=user.id).publish()
            self.send_message(text=text)
            self.start_send(user=user, text=text)
        else:
            ResumeManager(user_id=user.id).publish()
            self.send_message(text=text)

    def search_response(self, user):
        search = SearchManager(user_id=user.id).get()
        results = []

        if search:
            jobs = JobManager(user_id=user.id).get_vacations(search)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                text='◀️ Назад', switch_inline_query_current_chat='#jobs'))

            for job in jobs:
                text = f'<b>{job.looking_for}</b>\n\n' \
                       f'<b>Зарплата:</b> {job.wage}\n\n' \
                       f'<b>Город:</b> ' \
                       f'{job.city if job.city else "Отдаленная работа"}\n\n' \
                       f'<b>Опыт работы:</b> {job.experience}\n\n' \
                       f'<b>Описание вакансии:</b> {job.description}\n\n' \
                       f'<b>Написать работодателю:</b> {job.write_to_employer}'  # noqa

                results.append(InlineQueryResultArticle(
                    id=job.id,
                    title=job.looking_for,
                    description=f'{job.wage}\n{job.city if job.city else "Отдаленная работа"}',  # noqa
                    input_message_content=InputTextMessageContent(
                        message_text=text, parse_mode='HTML'),
                    thumb_url='https://telegra.ph/file/c5edf06f95fc5e4bda351.jpg',  # noqa
                    thumb_height=30,
                    thumb_width=30,
                    reply_markup=markup))
        if results:
            self.answer_inline_query(results=results)

    def search_sub_category(self, user, text):
        position = text.split(':')[-1]

        SearchManager(user_id=user.id).update_position(position=position)
        DialogSearchManager(user_id=user.id).update_position()

        search = SearchManager(user_id=user.id).get()

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            text='◀️ Назад',
            callback_data='◀️ Назад'))
        markup.add(InlineKeyboardButton(
            text='Найти',
            switch_inline_query_current_chat='#jobs'))

        text = f'<b>Ты выбрал!\n</b>Категорию: {search.category}\n'\
               f'Должность: {search.position}<a href="https:' \
               f'//telegra.ph/file/bb8803646002d244de091.jpg">&#160;</a>'

        self.edit_message_text(text=text, reply_markup=markup)

    def search_category(self, user, text):
        category = text.split(':')[-1]

        SearchManager(user_id=user.id).update_category(category=category)
        DialogSearchManager(user_id=user.id).update_category()

        self.send_sub_category(user=user, category=category)

    def check_search_category(self, user):
        return DialogSearchManager(user_id=user.id).check_category()

    def check_search_city(self, user):
        return DialogSearchManager(user_id=user.id).check_city()

    def search_city(self, user, text):
        valid = city_valid(city_name=text)

        if not valid:
            return self.send_message(text='нет такого города')

        search = SearchManager(user_id=user.id)
        search.clean()
        search.create_search(city=text)

        DialogSearchManager(user_id=user.id).update_city()

        self.send_categories(user=user)

    def check_search_start(self, user):
        return DialogSearchManager(user_id=user.id).check_start()

    def search_vacancy(self, user):
        dialog = DialogSearchManager(user_id=user.id)
        dialog.clean()
        dialog.start()
        text = self.text.search_vacancy()
        markup = self.markup.search_vacancy()
        self.send_message(text=text, reply_markup=markup)

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
                try:
                    self.edit_message_text(text=text, reply_markup=markup)
                except ApiException:
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
        markup = self.markup.experience()
        self.send_message(text=text, reply_markup=markup)

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

    def send_message(self, text, user_id=None, reply_markup=None):
        self.bot.send_message(
            chat_id=user_id or self.chat_id,
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

    def answer_inline_query(self, results):
        self.bot.answer_inline_query(
            inline_query_id=self.chat_id,
            results=results,
            cache_time=1,
            next_offset='',
            switch_pm_parameter='jobs',
            is_personal=True,
            switch_pm_text=f'Нашел [{len(results)}]'
        )

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
        elif user.profile == 2:
            ResumeManager(user_id=user.id).clean()
            dialog = DialogResumeManager(user_id=user.id)
            dialog.clean()
            dialog.create()

        text = self.text.send_categories()

        if self.check_search_city(user=user):
            reply_markup = self.markup.send_categories(search=True)
        else:
            reply_markup = self.markup.send_categories()

        try:
            self.edit_message_text(text=text, reply_markup=reply_markup)
        except ApiException:
            self.send_message(text=text, reply_markup=reply_markup)

    def send_sub_category(self, category, user):
        if user.profile == 1:
            JobManager(user_id=user.id).create(category=category)
            DialogJobManager(user_id=user.id).update_category()
        elif user.profile == 2:
            ResumeManager(user_id=user.id).create(category=category)
            DialogResumeManager(user_id=user.id).update_category()

        text = self.text.send_sub_category()

        if self.check_search_category(user=user):
            reply_markup = self.markup.send_sub_category(category, search=True)
        else:
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
        markup = self.markup.city()
        self.send_message(text=text, reply_markup=markup)

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
        markup = self.markup.experience()
        self.send_message(text=text, reply_markup=markup)

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
