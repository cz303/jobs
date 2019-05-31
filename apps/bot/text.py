class Text:
    def __init__(self, text=None):
        self.text = text

    def start_menu(self):
        self.text = "Выбери аккаунт, кем хочешь быть!"
        return self.text

    def employer(self):
        self.text = "Дальше"
        return self.text

    def worker(self):
        return self.employer()

    def tell_friends(self):
        self.text = '​​Я бот для поиска работы. С моей помощью ты можешь ' \
                    'быстро находить работу, или создавать свои вакансии и ' \
                    'искать кандидатов. Если тебе нравится моя работа, ' \
                    'то не забудь рассказать друзьям. ​​<a ' \
                    'href="https://telegra.ph/file/4539f1c1b87659d4f66ee.jpg' \
                    '"> &#160;</a>'
        return self.text

    def how_we_are_working(self):
        pass
