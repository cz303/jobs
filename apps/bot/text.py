import typing


class Text:
    def __init__(self, text: typing.Text = None):
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @text.deleter
    def text(self):
        del self._text

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

    def create_job(self):
        self.text = '<b>Вибери категорию!</b>\n Для того чтобы я смог делать' \
                    ' точные рассылки и показывать твою вакансию только' \
                    ' потенциальным кандидатам тебе нужно выбрать категорию.' \
                    '<a href="https://telegra.ph/file/4381281c14528aacd99ed' \
                    '.jpg"> &#160;</a>'
        return self.text
