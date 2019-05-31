from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

__all__ = ['Markup']


class Markup:
    def __init__(self):
        self.markup = ReplyKeyboardMarkup()
        self.markup.resize_keyboard = True

        self.inline = InlineKeyboardMarkup()

    def start_menu(self):
        self.markup.row(KeyboardButton(text='🏬 Работодатель'))
        self.markup.row(KeyboardButton(text='👨‍💻 Работник'))
        return self.markup

    def employer(self):
        self.markup.row(KeyboardButton(text='📬 Рассказать друзьям'))
        self.markup.row(KeyboardButton(text='Создать вакансию'))
        self.markup.row(KeyboardButton(text='Мои вакансии'))
        self.markup.row(KeyboardButton(text='Мой счет', request_contact=True))
        self.markup.row(KeyboardButton(text='Как мы работаем?'))
        self.markup.row(KeyboardButton(text='🏬 Изменить аккаунт'))
        return self.markup

    def worker(self):
        self.markup.row(KeyboardButton(text='📬 Рассказать друзьям'))
        self.markup.row(KeyboardButton(text='Создать резюме'))
        self.markup.row(KeyboardButton(text='Мои резюме'))
        self.markup.row(KeyboardButton(text='Поиск вакансий'))
        self.markup.row(KeyboardButton(text='Как мы работаем?'))
        self.markup.row(KeyboardButton(text='🏬 Изменить аккаунт'))
        return self.markup

    def tell_friends(self):
        self.inline.add(InlineKeyboardButton(
            text='Создать резюме',
            url='https://t.me/share/url?url=https%3A//telegram.me/RS_Work_bot'
        ))
