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

    def how_we_are_working(self, profile):
        if profile == 2:
            self.text = '<b>Как работает бот?</b>\nПосле публикации твоя ' \
                      'вакансия попадает в поиск вакансий,  где любой ' \
                      'заинтересованный кандидат сможет её найти.  Также мы ' \
                      'делаем рассылку только потенциальным кандидатам,  ' \
                      'которых может заинтересовать твоя вакансия. \n\n' \
                      '<b>Оплата!</b>\nПервая вакансия бесплатная, ' \
                      'следующие вакансии стоят 1 цент  за рассылку. 10 ' \
                      'кандидатов - 10 центов, 100 кандидатов - 1 ' \
                      'доллар.\n\n<b>Какой профессионализм ' \
                      'кандидатов?</b>\nЦена не влияет на профессионализм ' \
                      'наших кадров,  мы ведем такую ценовую политику, ' \
                      'при которой любой смог бы  найти кандидата без ' \
                      'дополнительной бюрократии, дёшево и быстро. ' \
                      'Мы хотим создать максимально комфортный сервис,' \
                      ' где за минимальную оплату ты получаешь лучшее ' \
                      'обслуживание для поиска работников.\n\n<b>Как мы ' \
                      'делаем рассылку?</b>\nКандидаты заполняют своё ' \
                      'резюме и на основе него мы можем  сделать точную ' \
                      'рассылку. Так что можешь быть уверен что твою  ' \
                      'вакансию увидят только потенциальные кандидаты,  ' \
                      'готовые работать.\n\n<b>Простота работы с ' \
                      'ботом!</b>\nНаша главная философия это скорость и ' \
                      'простота подачи вакансии.  Её может подать любой и ' \
                      'для этого не нужно подтверждать наличие  компании, ' \
                      'просто заходи и ищи нужных кандидатов.\n\n<b>Если я ' \
                      'оплатил меньше суммы которую указал бот?</b>\nТогда ' \
                      'бот сделает рассылку потенциальным кандидатам на ту  ' \
                      'сумму которую ты оплатил, с учетом 1 цент за одну ' \
                      'рассылку. Также вакансия добавится в поиск.'
        else:
            self.text = '<b>Как работает бот?</b>\nС помощью бота, ' \
                        'ты можешь искать интересные вакансии.  Мы ' \
                        'предлагаем только активные вакансии со сроком ' \
                        'подачи не более 7 дней. Также бот будет делать ' \
                        'постоянную рассылку только таких вакансий,' \
                        ' которые могут тебя заинтересовать.\n\n<b>Как мы ' \
                        'делаем рассылку?</b>\nТы получаешь рассылку на ' \
                        'основе своего резюме.  Данные резюме и вакансии ' \
                        'сравниваются и делается  точная рассылка. Так что ' \
                        'можешь быть уверенным,  что ты получишь только ' \
                        'нужную информацию, без всякого спама.\n\n' \
                        '<b>Простота работы с ботом!</b>\nТы можешь очень ' \
                        'быстро и бесплатно найти нужную  вакансию, ' \
                        'и непосредственно пообщаться с работодателем  в ' \
                        'Telegram. Если ты захочешь получать интересные  ' \
                        'вакансии, то просто быстро заполни краткое резюме ' \
                        'и получи лучшие предложения индивидуально для себя.',
        return self.text

    def send_categories(self):
        self.text = '<b>Вибери категорию!</b>\n Для того чтобы я смог делать' \
                    ' точные рассылки и показывать твою вакансию только' \
                    ' потенциальным кандидатам тебе нужно выбрать категорию.' \
                    '<a href="https://telegra.ph/file/4381281c14528aacd99ed' \
                    '.jpg"> &#160;</a>'
        return self.text

    def send_sub_category(self):
        self.text = '<b>Вибери под категорию!</b>\n' \
                    'Теперь выбери под категорию на которую ищешь работника.' \
                    ' Это позволит мне подобрать потенциальных кандидатов.' \
                    '<a href="https://telegra.ph/file/4381281c14528aacd99ed' \
                    '.jpg"> &#160;</a>'
        return self.text

    def looking_for(self):
        self.text = '<b>1. Кого ты ищешь?</b>\nОпиши кратко в одном ' \
                    'предложении, кто тебе нужен. Смотри пример в предыдущем' \
                    ' сообщении.<a ' \
                    'href="https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg' \
                    '">&#160;</a>'
        return self.text

    def wage(self):
        self.text = '<b>2. Заработная плата!</b>\nТеперь укажи размер ' \
                    'заработной платы, чтобы увеличить заинтересованность ' \
                    'у кандидатов. <a ' \
                    'href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def city(self):
        self.text = '<b>3. Город!</b>\nНапиши город где предлагается ' \
                    'данная вакансия, можно писать несколько городов ' \
                    'через запятую.<a ' \
                    'href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def experience(self):
        self.text = '<b>4. Опыт работы!</b>\nТеперь укажи, кандидатов ' \
                    'с каким опытом работы ты ищешь?<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#160;</a>'
        return self.text

    def description(self):
        self.text = '<b>5. Описание вакансии!</b>\nОпиши как можно ' \
                    'подробнее свою вакансию, это позволит увеличить ' \
                    'количество отзывов потенциальных кандидатов.' \
                    '<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#160;</a>'
        return self.text

    def write_to_employer(self):
        self.text = '<b>6. Написать работодателю!</b>\nУкажи свой username,' \
                    ' чтобы заинтересованные кандидаты могли с тобой' \
                    ' связаться.<a href="https:' \
                    '//telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def where_to_find_username_link(self):
        self.text = 'https://youtu.be/BSije4BPP7E'
        return self.text

    def where_to_find_username(self):
        self.text = 'Укажите пожалуйста свой username,' \
                    ' чтобы продолжить заполнение вакансий!'
        return self.text

    def moderation(self):
        self.text = '<b>Модерация!</b>\nВакансия отправлена на модерацию,' \
                    ' подожди пожалуйста. После модерации я пришлю тебе' \
                    ' готовый текст.<a href="https:' \
                    '//telegra.ph/file/8e149b7bf8849955c3212.jpg">&#160;</a>'
        return self.text

    def name(self):
        self.text = '<b>1. Имя!</b>\nУкажи свое имя, чтобы работодатель' \
                    ' знал как к тебе обращаться.' \
                    '<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#160;</a>'
        return self.text

    def age(self):
        self.text = '<b>2. Возраст!</b>\nУкажи свой возраст.<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#160;</a>'
        return self.text

    def work_city(self):
        self.text = '<b>3. Желаемый город работы!</b>\nУкажи город в' \
                    ' котором хочешь работать. Если хочешь работать ' \
                    'отдаленно, нажми кнопку - "Отдаленная работа".<a ' \
                    'href="https://telegra.ph/' \
                    'file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def lang(self):
        self.text = '<b>4. Языки!</b>\nЧерез запятую укажи какими языками ' \
                    'ты владеешь.<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def education(self):
        self.text = '<b>6. Образование!</b>\nУкажи где ты учился и в ' \
                    'течении какого периода.<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def work_experience(self):
        self.text = '<b>5. Опыт работы!</b>\nТеперь укажи свой опыт ' \
                    'работы на аналогичной должности. Это поможет быстрее ' \
                    'и точнее найти работу именно для тебя.' \
                    '<a href="https://telegra.ph/' \
                    'file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def work_description(self):
        self.text = '<b>7. О себе!</b>\nНапиши кратко о себе, чем ' \
                    'занимался, каковы твои положительные и отрицательные' \
                    ' черты, какие ожидания от работы. Не стесняйся ' \
                    'рассказать о своих достижениях :)<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#160;</a>'
        return self.text

    def work_moderation(self):
        self.text = 'Замечательно, резюме отправлено на модерацию, ' \
                    'подожди пожалуйста. После модерации я пришлю тебе ' \
                    'готовый текст.<a href="https://' \
                    'telegra.ph/file/8e149b7bf8849955c3212.jpg">&#160;</a>'
        return self.text

    def my_resume(self):
        self.text = "<b>Мои резюме!</b>\nНе забывай что вакансия " \
                    "активна 7 дней после чего ее нужно обновить." \
                    "​<a href='https://" \
                    "telegra.ph/file/301ec535e75c4d69d6f31.jpg'>&#160;</a>"
        return self.text

    def my_vacations(self):
        self.text = "<b>Мои вакансии!</b>\nНе забывай что вакансия " \
                    "активна 7 дней после чего ее нужно обновить." \
                    "​<a href='https://" \
                    "telegra.ph/file/301ec535e75c4d69d6f31.jpg'>&#160;</a>"
        return self.text

    def my_resume_on_moderation(self):
        self.text = "У вас ещё нет резюме. Чтобы создать резюме" \
                    " нажмите кнопку - <b>'Создать резюме'</b>."
        return self.text

    def my_vacation_on_moderation(self):
        self.text = "У вас ещё нет вакансий. Чтобы создать вакансию" \
                    " нажмите кнопку - <b>'Создать вакансию'</b>."
        return self.text

    def view_vacations(self, vacancy):
        self.text = f'<b>{vacancy.looking_for}</b>\n\n' \
                        f'<b>Зарплата:</b> {vacancy.wage}\n\n' \
                        f'<b>Город:</b> {vacancy.city}\n\n<b>' \
                        f'Опыт работы: {vacancy.experience}</b>\n\n' \
                        f'<b>Описание вакансии:</b>' \
                        f' {vacancy.description}\n\n' \
                        f'<b>Написать работодателю:</b>' \
                        f' @{vacancy.write_to_employer}' \
                        f"<a href='https:" \
                        f"//telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
                        f"&#160;</a>",
        return self.text
