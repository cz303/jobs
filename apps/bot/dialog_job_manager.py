from .models import JobDialog

__all__ = ['DialogJobManager']


class DialogJobManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self):
        JobDialog.objects.create(user_id=self.user_id, looking_for=True)

    def wage(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.looking_for = False
        job.wage = True
        job.save()

    def city(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.wage = False
        job.city = True
        job.save()

    def check_looking_for(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if job.looking_for:
            return True

    def check_wage(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()

        if job.wage:
            return True

    def check_city(self):
        job = JobDialog.objects.filter(
            user_id=self.user_id).order_by('-created').first()

        if job.city:
            return True
