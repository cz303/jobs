from .models import Resume

__all__ = ('ResumeManager',)


class ResumeManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, category):
        Resume.objects.create(
            user_id=self.user_id, category=category)

    def update_position(self, position):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.position = position
        resume.save()

    def update_name(self, name):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.name = name
        resume.save()

    def update_age(self, age):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.age = age
        resume.save()

    def update_city(self, city):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.city = city
        resume.save()

    def update_lang(self, lang):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.lang = lang
        resume.save()

    def update_experience(self, experience):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.experience = experience
        resume.save()

    def update_education(self, education):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.education = education
        resume.save()

    def update_description(self, description):
        resume = Resume.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.description = description
        resume.save()
