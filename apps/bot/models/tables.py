from django.db import models
from time import time, sleep
import requests
from django.conf import settings
import json
from .exeptions import FailureReasonError
from django.db.utils import IntegrityError


def get_score(user_id):
    user = User.objects.filter(user_id=user_id)[:1]

    if not user:
        return float(0)

    return user[0].credit


class User(models.Model):
    time = time()
    PROFILE = (
        (1, 'Работодатель'),
        (2, 'Работник')
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True, editable=False)
    user_id = models.IntegerField(null=False, unique=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True)
    credit = models.CharField(max_length=255, default=0.00)
    profile = models.SmallIntegerField(choices=PROFILE)
    created = models.DateTimeField(auto_now=True, editable=False)
    free_send = models.BooleanField(default=False)
    timestamp = models.IntegerField(default=time)

    def __str__(self):
        return self.username or str(self.user_id)

    def save(self, *args, **kwargs):
        credit = get_score(self.user_id)
        if float(self.credit) > float(credit):
            text = f"✅ Оплата прошла успешно!"
            requests.post(url=settings.URL,
                          data={f"chat_id": {str(self.user_id)},
                                "text": text,
                                "parse_mode": "HTML"})
            sleep(2.0)
            text = '<b>Как сделать рассылку вакансии?</b>\n\n1.Жми в меню' \
                   ' кнопку "Мои вакансии"\n\n' \
                   '2. Из списка своих вакансий,' \
                   ' вибери вакансию которую хочешь' \
                   ' разослать пользователям.\n\n3. В выбранной вакансии жми' \
                   ' кнопку "Сделать рассылку".<a href="https://' \
                   'telegra.ph/file/3b77208b93d61da309f3f.jpg">&#8205;</a>'
            requests.post(url=settings.URL,
                          data={f"chat_id": {str(self.user_id)},
                                "text": text,
                                "parse_mode": "HTML"})
        try:
            super().save(*args, **kwargs)
        except IntegrityError as error:
            print(str(error))


class Moderation:
    STATUS = (
        (1, 'В ожидании подтверждения'),
        (2, 'Подтвержденные'),
        (3, 'Отклоненные')
    )


class ICommonInfo(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    created = models.DateTimeField(auto_now=True, editable=False)
    timestamp = models.IntegerField(default=time)


class CommonInfo(ICommonInfo):
    class Meta:
        abstract = True

    category = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    remote = models.BooleanField(default=False)
    experience = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    moderation = models.IntegerField(choices=Moderation.STATUS, default=1)
    is_active = models.BooleanField(default=False)
    failure_reason = models.TextField(max_length=255, blank=True, null=True)
    publish = models.BooleanField(default=False)
    created = models.DateField(auto_now=True, editable=False)
    deleted = models.BooleanField(default=False)

    def reject(self):
        text = f"<b>❌ Ошибка!</b>\n<b>Причина:</b> {self.failure_reason}" \
            f"<a href='https://telegra.ph/file/dcc228d0b22135bbac896.jpg'>" \
            f"&#8205;</a>"
        requests.post(url=settings.URL,
                      data={f"chat_id": {str(self.user.user_id)},
                            "text": text,
                            "parse_mode": "HTML"})


class Job(CommonInfo):
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    looking_for = models.TextField(max_length=100, null=True, blank=True)
    wage = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    dispatch = models.IntegerField(default=0)
    write_to_employer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category

    def confirm(self):
        text = f'<b>{self.looking_for}</b>\n\n' \
            f'<b>Зарплата:</b> {self.wage}\n\n' \
            f'<b>Город:</b>' \
            f' {self.city if self.city else "Отдаленная работа"}\n\n' \
            f'<b>Опыт работы:</b> {self.experience}\n\n' \
            f'<b>Описание вакансии:</b> {self.description}\n\n' \
            f'<b>Написать работодателю:</b> {self.write_to_employer}' \
            f"<a href='https://" \
            f"telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
            f"&#8205;</a>"
        return requests.post(
            url=settings.URL,
            data={f"chat_id": {str(self.user.user_id)},
                  "text": {text},
                  "parse_mode": "HTML",
                  "reply_markup": json.dumps(
                      {"inline_keyboard": [
                          [{"text": "✅ Опубликовать",
                            "callback_data": f"free:{self.id}"}]]})})

    def save(self, *args, **kwargs):
        if self.moderation == 2 and not self.publish and not self.is_active:
            self.failure_reason = ''
            self.confirm()
        elif self.moderation == 3:
            if self.failure_reason == '':
                raise FailureReasonError(
                    'Поле "failure_reason" не должно быть пустым!')
            self.reject()

        super().save(*args, **kwargs)


class Resume(CommonInfo):
    class Meta:
        db_table = 'resumes'
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    name = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=255, null=True, blank=True)
    education = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.category

    def confirm(self):
        text = f'<b>Имя: </b>{self.name}\n\n' \
            f'<b>Возраст:</b> {self.age}\n\n' \
            f'<b>Желаемый город работы:</b>' \
            f' {self.city if self.city else "Отдаленная работа"}\n\n' \
            f'<b>Языки:</b> {self.lang}\n\n' \
            f'<b>Опыт работы:</b> {self.experience}\n\n' \
            f'<b>Образование: </b> {self.education}\n\n' \
            f'<b>О себе:</b> {self.description}' \
            f"<a href='https://" \
            f"telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
            f"&#8205;</a>"
        return requests.post(
            url=settings.URL,
            data={
                f"chat_id": {
                    str(self.user.user_id)
                },
                "text": {
                    text
                },
                "parse_mode": "HTML",
                "reply_markup": json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "✅ Опубликовать",
                                    "callback_data": "✅ Опубликовать"
                                }
                            ]
                        ]
                    }
                )
            }
        )

    def save(self, *args, **kwargs):
        if self.moderation == 2 and not self.publish and not self.is_active:
            self.failure_reason = ''
            self.confirm()
        elif self.moderation == 3:
            if self.failure_reason == '':
                raise FailureReasonError(
                    'Поле "failure_reason" не должно быть пустым!')
            self.reject()

        super().save(*args, **kwargs)


class City(models.Model):
    class Meta:
        db_table = 'city'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Statistics(models.Model):
    class Meta:
        db_table = 'statistics'

    id = models.AutoField(primary_key=True, editable=False)
    # who did the newsletter
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # who sent the list from id
    sent_to_users = models.CharField(max_length=500, blank=True)
    # number sent out
    count = models.IntegerField()
    # price of one mailing
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.02)
    # spent money for the newsletter
    funds_spent = models.DecimalField(max_digits=8, decimal_places=2,
                                      default=0.00)
    created = models.DateField(auto_now=True, editable=False)
    # free send default 10
    free_send = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username


class IDialog(ICommonInfo):
    class Meta:
        abstract = True

    city = models.BooleanField(default=False)
    remote = models.BooleanField(default=False)
    experience = models.BooleanField(default=False)
    description = models.BooleanField(default=False)
    category = models.BooleanField(default=False)
    position = models.BooleanField(default=False)


class JobDialog(IDialog):
    class Meta:
        db_table = 'jobdialog'

    looking_for = models.BooleanField(default=False)
    wage = models.BooleanField(default=False)
    write_to_employer = models.BooleanField(default=False)
    create_job = models.BooleanField(default=False)


class ResumeDialog(IDialog):
    class Meta:
        db_table = 'resumedialog'

    create_resume = models.BooleanField(default=False)
    name = models.BooleanField(default=False)
    age = models.BooleanField(default=False)
    lang = models.BooleanField(default=False)
    education = models.BooleanField(default=False)


class Searching(ICommonInfo):
    start = models.BooleanField(default=False)
    city = models.BooleanField(default=False)
    category = models.BooleanField(default=False)
    position = models.BooleanField(default=False)


class Search(ICommonInfo):
    category = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)


class SendDialog(ICommonInfo):
    checker_start = models.BooleanField(default=False)
    resume_id = models.IntegerField(null=True, blank=True)
    candidates = models.TextField(max_length=2000, blank=True)
    count = models.IntegerField(default=0)
