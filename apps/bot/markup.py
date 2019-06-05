from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from collections import defaultdict
import itertools

__all__ = ['Markup']


class Markup:
    def __init__(self):
        self.markup = ReplyKeyboardMarkup()
        self.markup.resize_keyboard = True
        self.markup.one_time_keyboard = True

        self.inline = InlineKeyboardMarkup()

    def send(self, texts: list, inline=None):
        if inline:
            for text in texts:
                if text == 'Отправить!':
                    self.inline.add(InlineKeyboardButton(
                        text=text,
                        callback_data=text,
                        url='https://t.me/share/url?url=https%3A//telegram'
                            '.me/RS_Work_bot'))
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
            'Специалист по обучению персонала',
            'Специалист по охране труда',
            'Психолог',
            'Инженер']
        data['2. IT, WEB специалисты'] = [
            '◀️ Назад',
            'CEO | Product Manager',
            '​​​​​​​Java',
            'C# | .NET',
            'JavaScript | Front-End | HTML',
            'Node.js',
            'PHP',
            'Python',
            'Ruby',
            'Android',
            'iOS | macOS',
            'C | C++ | Embedded',
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

    def send_categories(self):
        return self.send(self.categories, inline=True)

    def get_category(self, category: str):
        return defaultdict(list, filter(lambda x: x[0] == category,
                                        self.get_data().items()))

    def send_sub_category(self, category):
        return self.send(self.get_category(
            category=category).get(category, []), inline=True)

    def write_to_employer(self):
        texts = ['Где искать username?']
        return self.send(texts=texts, inline=True)
