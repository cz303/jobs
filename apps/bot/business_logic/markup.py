from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from collections import defaultdict
import itertools

__all__ = ('Markup',)


class Markup:
    def __init__(self):
        self.markup = ReplyKeyboardMarkup()
        self.markup.resize_keyboard = True
        self.markup.one_time_keyboard = True

        self.inline = InlineKeyboardMarkup()

    def send(self, texts=None, callback_data=None, inline=None, url=None):
        if isinstance(callback_data, list):
            for k, v in callback_data:
                self.inline.add(InlineKeyboardButton(text=k, callback_data=v))
            return self.inline

        if inline:
            for text in texts:
                if text == 'Отправить!':
                    self.inline.add(InlineKeyboardButton(
                        text=text,
                        callback_data=callback_data or text,
                        url='https://t.me/share/url?url=https%3A//telegram'
                            '.me/RS_Work_bot'))
                    return self.inline
                elif text == 'Оплатить':
                    self.inline.add(InlineKeyboardButton(
                        text=text,
                        callback_data=callback_data or text,
                        url=url
                    ))
                    return self.inline

                self.inline.add(InlineKeyboardButton(text=text,
                                                     callback_data=text))
            return self.inline

        for text in texts:
            if text == 'Мой счет':
                self.markup.row(
                    KeyboardButton(text=text, request_contact=True))
            else:
                self.markup.row(KeyboardButton(text=text))
        return self.markup

    def start_menu(self):
        texts = ['🏬 Работодатель', '👨‍💻 Работник']
        return self.send(texts)

    def employer(self):
        texts = ['📬 Рассказать друзьям', 'Создать вакансию', 'Мои вакансии',
                 'Мой счет', 'Как мы работаем?', '🏬 Изменить аккаунт']
        return self.send(texts)

    def worker(self):
        texts = ['📬 Рассказать друзьям', 'Создать резюме', 'Мои резюме',
                 'Поиск вакансий', 'Как мы работаем?', '🏬 Изменить аккаунт']
        return self.send(texts)

    def tell_friends(self):
        texts = ['Отправить!']
        return self.send(texts=texts, inline=True)

    @classmethod
    def get_data(cls):
        data = defaultdict(list)
        data['1. HR, управление персоналом'] = [
            '◀️ Назад',
            'Менеджер',
            'Рекрутер',
            'Инспектор',
            'Специалист персонала',
            'Специалист по охране труда',
            'Психолог',
            'Инженер']
        data['2. IT, WEB специалисты'] = [
            '◀️ Назад',
            'CEO | Product Manager',
            '​​​​​​​Java',
            'C# | .NET',
            'JavaScript',
            'Node.js',
            'PHP',
            'Python',
            'Ruby',
            'Android',
            'iOS | macOS',
            'C | C++',
            'Golang',
            'Scala',
            'Дизайнери | UI | UX',
            'QA Automation | Manual',
            'Project Manager',
            'DevOps | Sysadmin']
        return data

    @property
    def categories(self):
        return list(map(lambda x: x, self.get_data().keys()))

    @property
    def get_sub_categories(self):
        return list(itertools.chain(*self.get_data().values()))

    def send_categories(self, search=None):
        if search:
            data = []

            for category in self.categories:
                data.append((category, f'search:{category}'))

            return self.send(callback_data=data, inline=True)
        else:
            return self.send(self.categories, inline=True)

    def get_category(self, category: str):
        return defaultdict(list, filter(lambda x: x[0] == category,
                                        self.get_data().items()))

    def send_sub_category(self, category, search=None):
        categories = self.get_category(category=category).get(category, [])

        if search:
            data = []

            for category in categories:
                if category == '◀️ Назад':
                    data.append((category, category))
                else:
                    data.append((category, f's:{category}'))

            return self.send(callback_data=data, inline=True)
        else:
            return self.send(categories, inline=True)

    def write_to_employer(self):
        texts = ['Где искать username?']
        return self.send(texts=texts, inline=True)

    def my_resume(self, resumes):
        data = []
        for resume in resumes:
            if resume.moderation == 2:
                if resume.is_active:
                    data.append(
                        (f"{resume.position[:22]}...",
                         f"resumes:{resume.is_active}:{resume.id}"))
                else:
                    # add icon update
                    data.append((f"🔄  {resume.position[:22]}...",
                                 f"resumes:{resume.id}"))

        return self.send(callback_data=data, inline=True)

    def my_vacations(self, vacations):
        data = []
        for vacation in vacations:
            if vacation.moderation == 2:
                if vacation.is_active:
                    data.append(
                        (f"{vacation.position[:22]}...",
                         f"vacations:{vacation.is_active}:{vacation.id}"))
                else:
                    # add icon update
                    data.append(
                        (f"🔄  {vacation.position[:22]}...",
                         f"vacations:{vacation.id}"))

        return self.send(callback_data=data, inline=True)

    def view_vacations(self, vacancy):
        if not vacancy.is_active:
            item = ('🔄 Обновить', f'v:update:{vacancy.id}')
        else:
            item = ('Удалить', f'v:del:{vacancy.id}')

        data = [('◀️ Назад', 'v:return'),
                ('Сделать рассылку', f'send:{vacancy.id}'),
                item]

        return self.send(callback_data=data, inline=True)

    def view_resume(self, resume):
        if not resume.is_active:
            item = ('🔄 Обновить', f'r:update:{resume.id}')
        else:
            item = ('Удалить', f'r:del:{resume.id}')

        data = [('◀️ Назад', 'r:return'), item]

        return self.send(callback_data=data, inline=True)

    def search_vacancy(self):
        texts = ['Отдалённая работа']
        return self.send(texts, inline=True)

    def publish(self):
        texts = ['✅ Начать']
        return self.send(texts, inline=True)

    def my_score(self):
        texts = ['Оплатить в: USD(доллар)']
        return self.send(texts, inline=True)

    @classmethod
    def pay_buttons(cls):
        return ['Оплатить 1 $', 'Оплатить 3 $', 'Оплатить 5 $',
                'Оплатить 10 $', 'Оплатить 25 $']

    def pay(self):
        texts = self.pay_buttons()
        return self.send(texts, inline=True)

    def liq(self, url):
        texts = ['Оплатить']
        return self.send(texts=texts, inline=True, url=url)

    def city(self):
        texts = ['Отдалённая работа']
        return self.send(texts=texts, inline=True)

    def experience(self):
        texts = ['Нет опыта', '1 год', '2 года', '3 года', '5 лет']
        return self.send(texts=texts, inline=True)

    def confirmation_send(self):
        texts = ['✅ Я согласен']
        return self.send(texts=texts, inline=True)
