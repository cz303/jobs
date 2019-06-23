from bot.models.tables import JobDialog
from .base_manager import Manager


class DialogJobManager(Manager):

    def create(self):
        JobDialog.objects.create(user_id=self.user_id, create_job=True)

    def update_category(self):
        job = JobDialog.objects.filter(user_id=self.user_id).first()
        job.create_job = False
        job.category = True
        job.save()

    def update_position(self):
        job = JobDialog.objects.filter(user_id=self.user_id).first()
        job.category = False
        job.position = True
        job.save()

    def looking_for(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).first()
        job.position = False
        job.looking_for = True
        job.save()

    def wage(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).first()
        job.looking_for = False
        job.wage = True
        job.save()

    def city(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).first()
        job.wage = False
        job.city = True
        job.save()

    def experience(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.city = False
        job.experience = True
        job.save()

    def description(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.experience = False
        job.description = True
        job.save()

    def write_to_employer(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.description = False
        job.write_to_employer = True
        job.save()

    def clean(self):
        JobDialog.objects.filter(user_id=self.user_id).delete()

    def check_looking_for(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.looking_for

    def check_wage(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.wage

    def check_city(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.city

    def check_experience(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.experience

    def check_description(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.description

    def check_write_to_employer(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not job:
            return False
        else:
            return job.write_to_employer
