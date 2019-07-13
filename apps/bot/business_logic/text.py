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
                    'то не забудь рассказать друзьям.​​<a href="https://' \
                    'telegra.ph/file/4539f1c1b87659d4f66ee.jpg">&#8205;</a>'
        return self.text

    def how_we_are_working(self, profile):
        if profile == 2:
            self.text = '<b>Как работает бот?</b>\nПосле публикации твоя ' \
                      'вакансия попадает в поиск вакансий,  где любой ' \
                      'заинтересованный кандидат сможет её найти.  Также мы ' \
                      'делаем рассылку только потенциальным кандидатам,  ' \
                      'которых может заинтересовать твоя вакансия. \n\n' \
                      '<b>Оплата!</b>\nПервая вакансия бесплатная, ' \
                      'следующие вакансии стоят 2 цента  за рассылку. 10 ' \
                      'кандидатов - 20 центов, 100 кандидатов - 2 ' \
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
                      'сумму которую ты оплатил, с учетом 2 цента за одну ' \
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
                        'и получи лучшие предложения индивидуально для себя.'
        return self.text

    def send_categories(self):
        self.text = '<b>Вибери категорию!</b>\nДля того чтобы я смог делать' \
                    ' точные рассылки и показывать твою вакансию только' \
                    ' потенциальным кандидатам, тебе нужно выбрать категорию.'\
                    '<a href="https://' \
                    'telegra.ph/file/4381281c14528aacd99ed.jpg">&#8205;</a>'
        return self.text

    def send_sub_category(self):
        self.text = '<b>Вибери под категорию!</b>\n' \
                    'Теперь выбери под категорию на которую ищешь работника.' \
                    ' Это позволит мне подобрать потенциальных кандидатов.' \
                    '<a href="https://telegra.ph/file/4381281c14528aacd99ed' \
                    '.jpg">&#8205;</a>'
        return self.text

    def looking_for(self):
        self.text = '<b>1. Кого ты ищешь?</b>\nОпиши кратко в одном ' \
                    'предложении, кто тебе нужен. Например: Ищу разработчика '\
                    'ботов на python.<a ' \
                    'href="https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg' \
                    '">&#8205;</a>'
        return self.text

    def wage(self):
        self.text = '<b>2. Заработная плата!</b>\nТеперь укажи размер ' \
                    'заработной платы, чтобы увеличить заинтересованность ' \
                    'у кандидатов. <a ' \
                    'href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def city(self):
        self.text = '<b>3. Город!</b>\nНапиши город где предлагается ' \
                    'данная вакансия, можно писать несколько городов ' \
                    'через запятую.<a ' \
                    'href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def experience(self):
        self.text = '<b>4. Опыт работы!</b>\nТеперь укажи, кандидатов ' \
                    'с каким опытом работы ты ищешь?<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#8205;</a>'
        return self.text

    def description(self):
        self.text = '<b>5. Описание вакансии!</b>\nОпиши как можно ' \
                    'подробнее свою вакансию, это позволит увеличить ' \
                    'количество отзывов потенциальных кандидатов.' \
                    '<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#8205;</a>'
        return self.text

    def write_to_employer(self):
        self.text = '<b>6. Написать работодателю!</b>\nУкажи свой username,' \
                    ' чтобы заинтересованные кандидаты могли с тобой' \
                    ' связаться.<a href="https:' \
                    '//telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
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
                    ' подожди пожалуйста. После модерации я отправлю тебе' \
                    ' готовый текст.<a href="https:' \
                    '//telegra.ph/file/8e149b7bf8849955c3212.jpg">&#8205;</a>'
        return self.text

    def name(self):
        self.text = '<b>1. Имя!</b>\nУкажи свое имя, чтобы работодатель' \
                    ' знал как к тебе обращаться.' \
                    '<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#8205;</a>'
        return self.text

    def age(self):
        self.text = '<b>2. Возраст!</b>\nУкажи свой возраст.<a href=' \
                    '"https://telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">' \
                    '&#8205;</a>'
        return self.text

    def work_city(self):
        self.text = '<b>3. Желаемый город работы!</b>\nУкажи город в' \
                    ' котором хочешь работать. Если хочешь работать ' \
                    'отдаленно, нажми кнопку - "Отдаленная работа".<a ' \
                    'href="https://telegra.ph/' \
                    'file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def lang(self):
        self.text = '<b>4. Языки!</b>\nЧерез запятую укажи какими языками ' \
                    'ты владеешь.<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def education(self):
        self.text = '<b>6. Образование!</b>\nУкажи где ты учился и в ' \
                    'течении какого периода.<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def work_experience(self):
        self.text = '<b>5. Опыт работы!</b>\nТеперь укажи свой опыт ' \
                    'работы на аналогичной должности. Это поможет быстрее ' \
                    'и точнее найти работу именно для тебя.' \
                    '<a href="https://telegra.ph/' \
                    'file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def work_description(self):
        self.text = '<b>7. О себе!</b>\nНапиши кратко о себе, чем ' \
                    'занимался, каковы твои положительные и отрицательные' \
                    ' черты, какие ожидания от работы. Не стесняйся ' \
                    'рассказать о своих достижениях :)<a href="https://' \
                    'telegra.ph/file/69270e02b6ad3bdd6a2b5.jpg">&#8205;</a>'
        return self.text

    def work_moderation(self):
        self.text = 'Замечательно, резюме отправлено на модерацию, ' \
                    'подожди пожалуйста. После модерации я пришлю тебе ' \
                    'готовый текст.<a href="https://' \
                    'telegra.ph/file/8e149b7bf8849955c3212.jpg">&#8205;</a>'
        return self.text

    def my_resume(self):
        self.text = "<b>Мои резюме!</b>\nНе забывай что резюме " \
                    "активна 7 дней после чего ее нужно обновить." \
                    "​<a href='https://" \
                    "telegra.ph/file/301ec535e75c4d69d6f31.jpg'>&#8205;</a>"
        return self.text

    def my_vacations(self):
        self.text = "<b>Мои вакансии!</b>\nНе забывай что вакансия " \
                    "активна 7 дней после чего ее нужно обновить." \
                    "​<a href='https://" \
                    "telegra.ph/file/301ec535e75c4d69d6f31.jpg'>&#8205;</a>"
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
                        f' {vacancy.write_to_employer}' \
                        f"<a href='https:" \
                        f"//telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
                        f"&#8205;</a>"
        return self.text

    def view_resume(self, resume):
        self.text = f'<b>Имя: </b>{resume.name}\n\n' \
                    f'<b>Возраст:</b> {resume.age}\n\n' \
                    f'<b>Желаемый город работы:</b>' \
                    f' {resume.city if resume.city else "Отдаленная работа"}' \
                    f'\n\n<b>Языки:</b> {resume.lang}\n\n' \
                    f'<b>Опыт работы:</b> {resume.experience}\n\n' \
                    f'<b>Образование: </b> {resume.education}\n\n'\
                    f'<b>О себе:</b> {resume.description}' \
                    f"<a href='https://" \
                    f"telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
                    f"&#8205;</a>"
        return self.text

    def search_vacancy(self):
        self.text = '<b>Выбери город!</b>\nВ каком городе ты ищешь вакансию?' \
                    ' Напиши правильно название своего города, или нажми' \
                    ' кнопку отдалённая работа.<a href="https://' \
                    'telegra.ph/file/a316fb315bc81d9191e85.jpg">&#8205;</a>'
        return self.text

    def publish(self, user):
        if user.profile == 2:
            self.text = '<b>Резюме опубликовано!</b>\n' \
                   'Я буду присылать только актуальные вакансии,' \
                   ' которые могут тебя заинтересовать. Также ты можешь' \
                   ' самостоятельно искать вакансии,' \
                   ' используй кнопку - "Поиск вакансий".<a href="https://' \
                   'telegra.ph/file/61fa97040248dfe91fde6.jpg">&#8205;</a>'
        else:
            self.text = '✅ <b>Делаю рассылку!</b>\nЯ сделаю бесплатную ' \
                        'рассылку твоей вакансии 10 потенциальным кандидатам,'\
                        ' которых она может заинтересовать. А также ' \
                        'добавлю её в поиск.<a href="https://' \
                   'telegra.ph/file/8082b45ad06ea8bc2805e.jpg">&#8205;</a>'
        return self.text

    def my_score(self, balance):
        balance = round(float(balance), 2)
        self.text = '<b>Мой счёт!</b>\nЧтобы начать продвижение ' \
                    'твоей вакансии, на счету должно быть' \
                    ' минимум 0.02$\n1 рассылка = 2 цента\n\n💰<b>' \
                    f'{balance}$</b><a href="https://' \
                    f'telegra.ph/file/8082b45ad06ea8bc2805e.jpg">&#8205;</a>'
        return self.text

    def pay(self):
        self.text = '<b>Выбери сумму оплаты!</b>\n' \
                    '1 рассылка = 2 цента<a href="https://' \
                    'telegra.ph/file/8082b45ad06ea8bc2805e.jpg">&#8205;</a>'
        return self.text

    def redirect_to_liq_error(self):
        self.text = 'Произошла ошибка. Попробуйте позже.'
        return self.text

    def liq(self, count, value):
        self.text = f'<b>К оплате - {count}{value}</b><a href="https://' \
                    f'telegra.ph/file/8082b45ad06ea8bc2805e.jpg">&#8205;</a>'
        return self.text

    def top_up_account(self, balance):
        self.text = '<b>Нужно пополнить счёт!</b>\n10 бесплатных рассылок' \
                    ' закончились. Чтобы продолжить продвижение своей ' \
                    f'вакансии, сделай оплату.💰\n' \
                    f'<b>1 рассылка = 2 цента</b>\n\n' \
                    f'<b>{round(float(balance), 2)}$</b><a href="https://' \
                    f'telegra.ph/file/a95582839314e44a6fcc1.jpg">&#8205;</a>'
        return self.text

    def not_jobs(self):
        self.text = '<b>По вашему запросу вакансий еще нет!</b>' \
                    '<a href="https://' \
                    'telegra.ph/file/4539f1c1b87659d4f66ee.jpg">&#8205;</a>'
        return self.text

    def start_send(self):
        self.text = '<b>Начинаю продвижение вакансии!</b><a href="https://' \
                    'telegra.ph/file/4539f1c1b87659d4f66ee.jpg">&#8205;</a>'
        return self.text

    def send_resume(self, job):
        self.text = f"<b>Появилась новая вакансия по твоему профилю:" \
                        f"</b>\n\n<b>Ищу: {job.looking_for}</b>\n\n" \
                        f"<b>Зарплата:</b> {job.wage}\n\n<b>Город:</b>" \
                        f" {job.city or 'Отдаленная работа'}\n\n" \
                        f"<b>Опыт работы:</b>" \
                        f" {job.experience}\n\n<b>Описание вакансии:</b>" \
                        f" {job.description}\n\n" \
                        f"<b>Написать работодателю:</b>" \
                        f" {job.write_to_employer}"
        return self.text

    def statistics(self, count, price, funds_spent, credit=None,
                   free_send=None, free_send_count=None):
        msg = "пользователям" if count > 1 else "пользователю"
        if credit:
            row = f"Потрачено средств: {funds_spent}$\n\n" \
                  f"<b>{round(credit, 2)}$</b>'"
        else:
            row = f"Потрачено бессплатных рассылок: {free_send}\n\n" \
                  f"Осталось: {free_send_count} рассылок"
        self.text = '<b>📊Статистика по рассылке вакансии:</b>\n\n' \
                    f'Сделана рассылка: {count} {msg}\n' \
                    f'Цена одного сообщения: {price}$ (2 цента)\n' \
                    f'{row}<a href="https://' \
                    'telegra.ph/file/e56a1c86e5c97e6b5f818.jpg">&#8205;</a>'
        return self.text

    def free_send(self):
        self.text = '<b>10 Бесплатных рассылок!</b>\nЯ сделаю бесплатную' \
                    ' рассылку твоей вакансии 10 потенциальным кандидатам,' \
                    ' которых она может заинтересовать.' \
                    ' А также добавлю её в поиск.<a href="https://' \
                    'telegra.ph/file/fcae07d115897438db7b6.jpg">&#8205;</a>'
        return self.text

    def why_send(self):
        self.text = '<b>Как сделать рассылку вакансии?</b>\nЖми в меню' \
                    ' кнопку "Мои вакансии", вибери вакансию которую хочешь' \
                    ' разослать пользователям. В выбранной вакансии жми' \
                    ' кнопку "Сделать рассылку".<a href="https://' \
                    'telegra.ph/file/bf4a40c5d54b8330b2424.jpg">&#8205;</a>'
        return self.text

    def found_candidates(self, candidates, balance):
        self.text = f'<b>Найдено {candidates} кандидатов.</b>\n\n' \
                    f'Напиши числом, скольким кандидатам сделать рассылку?\n' \
                    f'1 рассылка = 2 цента\n\n💰<b>' \
                    f'{round(float(balance), 2)}$</b>' \
                    f'<a href="https://' \
                    'telegra.ph/file/22bce89e5ee8c1f25806c.jpg">&#8205;</a>'
        return self.text

    def confirmation_send(self, can, price, balance):
        balance = round(float(balance), 2)
        self.text = f'<b>Делаю рассылку {can} кандидатам!</b>\n' \
                    f'Цена рассылки: {price}$\n\n' \
                    f'💰<b>{balance}$</b><a href="https://' \
                    f'telegra.ph/file/22bce89e5ee8c1f25806c.jpg">&#8205;</a>'
        return self.text

    def complete_send(self):
        self.text = '✅ Рассылка вакансии успешно сделана!'
        return self.text
