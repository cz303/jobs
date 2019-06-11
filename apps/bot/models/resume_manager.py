from bot.models.tables import Resume

__all__ = ('ResumeManager',)


class ResumeManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, category):
        Resume.objects.create(
            user_id=self.user_id, category=category)

    def clean(self):
        Resume.objects.filter(user_id=self.user_id, position=None).delete()

    def update_position(self, position):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.position = position
        resume.save()

    def update_name(self, name):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.name = name
        resume.save()

    def update_age(self, age):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.age = age
        resume.save()

    def update_city(self, city):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.city = city
        resume.save()

    def update_lang(self, lang):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.lang = lang
        resume.save()

    def update_experience(self, experience):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.experience = experience
        resume.save()

    def update_education(self, education):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.education = education
        resume.save()

    def update_description(self, description):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        resume.description = description
        resume.save()

    def get_resume(self):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse()
        return resume
