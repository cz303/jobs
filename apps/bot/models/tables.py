from django.db import models
from time import time
import requests
from django.conf import settings
import json
from .exeptions import FailureReasonError


class User(models.Model):
    time = time()
    PROFILE = (
        (1, 'Работодатель'),
        (2, 'Работник')
    )

    class Meta:
        db_table = 'users'

    id = models.AutoField(primary_key=True, editable=False)
    user_id = models.IntegerField(null=False, unique=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True)
    credit = models.CharField(max_length=255, default=0.00)
    profile = models.SmallIntegerField(choices=PROFILE)
    created = models.DateTimeField(auto_now=True, editable=False)
    timestamp = models.IntegerField(default=time)

    def __str__(self):
        return self.username


class Moderation:
    STATUS = (
        (1, 'Waiting for verification'),
        (2, 'Confirmed'),
        (3, 'Rejected')
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
    experience = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=1000, null=True)
    moderation = models.IntegerField(choices=Moderation.STATUS, default=1)
    is_active = models.BooleanField(default=False)
    failure_reason = models.TextField(max_length=255, blank=True, null=True)
    publish = models.BooleanField(default=False)
    created = models.DateField(auto_now=True, editable=False)
    deleted = models.BooleanField(default=False)

    def reject(self):
        text = f"<b>❌ Ошибка!</b>\n{self.failure_reason}\n\n" \
            f"Исправь ошибку, которая указана выше," \
            f" и создай вакансию заново, нажми кнопку 'Создать вакансию'.\n\n"\
            f"<a href='https://telegra.ph/file/98cad48a0b2343f710f96.jpg'>" \
            f"&#160;</a>"
        requests.post(url=settings.URL,
                      data={f"chat_id": {str(self.user.user_id)},
                            "text": text,
                            "parse_mode": "HTML"})


class Job(CommonInfo):
    class Meta:
        db_table = 'jobs'

    looking_for = models.TextField(max_length=255, null=True)
    wage = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    dispatch = models.IntegerField(default=0)
    write_to_employer = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.category

    def confirm(self):
        text = f'<b>{self.looking_for}</b>\n\n' \
            f'<b>Зарплата:</b> {self.wage}\n\n' \
            f'<b>Город:</b>' \
            f' {self.city if self.city else "Отдаленная работа"}\n\n' \
            f'<b>Опыт работы:</b> {self.experience}\n\n' \
            f'<b>Описание вакансии:</b> {self.description}\n\n' \
            f'<b>Написать работодателю:</b> @{self.write_to_employer}\n\n' \
            f"<a href='https://" \
            f"telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
            f"&#160;</a>"
        return requests.post(
            url=settings.URL,
            data={f"chat_id": {str(self.user.user_id)},
                  "text": {text},
                  "parse_mode": "HTML",
                  "reply_markup": json.dumps(
                      {"inline_keyboard": [
                          [{"text": "✅ Опубликовать",
                            "callback_data": "✅ Опубликовать"}]]})})

    def save(self, *args, **kwargs):
        if self.moderation == 2:
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

    name = models.CharField(max_length=255, null=True)
    age = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=255, null=True)
    education = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.category

    def confirm(self):
        text = f'<b>Имя: </b>{self.name}\n\n' \
            f'<b>Возвраст:</b> {self.age}\n\n' \
            f'<b>Желаемый город работы:</b>' \
            f' {self.city if self.city else "Отдаленная работа"}\n\n' \
            f'<b>Языки:</b> {self.lang}\n\n' \
            f'<b>Опыт работы:</b> {self.experience}\n\n' \
            f'<b>Образование: </b> {self.education}\n\n' \
            f'<b>О себе:</b> {self.description}' \
            f"<a href='https://" \
            f"telegra.ph/file/f03179992f64479dc4b20.jpg'>" \
            f"&#160;</a>"
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
        if self.moderation == 2:
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
    sent = models.CharField(max_length=500, blank=True)
    # number sent out
    count = models.IntegerField()
    # price of one mailing
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.02)
    # spent money for the newsletter
    funds_spent = models.DecimalField(max_digits=8, decimal_places=2,
                                      default=0.00)
    created = models.DateField(auto_now=True, editable=False)

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
