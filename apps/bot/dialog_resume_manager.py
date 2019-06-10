from .models import ResumeDialog

__all__ = ('DialogResumeManager',)


class DialogResumeManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self):
        ResumeDialog.objects.create(user_id=self.user_id, create_job=True)

    def update_category(self):
        job = ResumeDialog.objects.filter(user_id=self.user_id).first()
        job.create_job = False
        job.category = True
        job.save()

    def update_position(self):
        job = ResumeDialog.objects.filter(user_id=self.user_id).first()
        job.category = False
        job.position = True
        job.save()

    def age(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.name = False
        resume.age = True
        resume.save()

    def city(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.age = False
        resume.city = True
        resume.save()

    def lang(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.city = False
        resume.lang = True
        resume.save()

    def experience(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.lang = False
        resume.experience = True
        resume.save()

    def education(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.experience = False
        resume.education = True
        resume.save()

    def description(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        resume.education = False
        resume.description = True
        resume.save()

    def clean(self):
        ResumeDialog.objects.filter(user_id=self.user_id).delete()

    def check_name(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.name

    def check_age(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.age

    def check_city(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.city

    def check_lang(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.lang

    def check_experience(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.experience

    def check_education(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.education

    def check_description(self):
        resume = ResumeDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not resume:
            return False
        else:
            return resume.description
