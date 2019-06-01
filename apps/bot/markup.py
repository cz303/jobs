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
        texts = ['🏬 Работодатель', '👨‍💻 Работник']
        return self.create(texts)

    def create(self, texts: list, inline=None):
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

    def employer(self):
        texts = ['📬 Рассказать друзьям', 'Создать вакансию', 'Мои вакансии',
                 'Мой счет', 'Как мы работаем?', '🏬 Изменить аккаунт']
        return self.create(texts)

    def worker(self):
        texts = ['📬 Рассказать друзьям', 'Создать резюме', 'Мои резюме',
                 'Поиск вакансий', 'Как мы работаем?', '🏬 Изменить аккаунт']
        return self.create(texts)

    def tell_friends(self):
        texts = ['Отправить!']
        return self.create(texts=texts, inline=True)

    @property
    def categories(self):
        return [
            '1. HR, управление персоналом',
            '2. IT, WEB специалисты',
            '3. Работа для студентов',
            '4. Реклама, маркетинг, PR',
            '5. Бухгалтерия, финансы, учет | аудит',
            '6. Туризм и спорт',
            '7. Юриспруденция, право',
            '8. Гостиничный бизнес',
            '9. Дизайн, творчество',
            '10. Домашний сервис',
            '11. Консалтинг',
            '12. Красота и SPA-услуги',
            '13. Логистика, доставка, склад',
            '14. Медицина, фармацевтика',
            '15. Недвижимость и страхование',
            '16. Офисный персонал',
            '17. Ресторанный бизнес, кулинария',
            '18. Сельское хозяйство, агробизнеc',
            '19. Сфера развлечений',
            '20. Торговля, продажи, закупки',
            '21. Транспорт, автосервис'
        ]

    def create_job(self):
        return self.create(self.categories, inline=True)
