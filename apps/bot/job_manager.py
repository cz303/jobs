from .models import Job

__all__ = ['JobManager']


class JobManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, category):
        Job.objects.create(
            user_id=self.user_id, category=category)

    def update_position(self, position):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.position = position
        job.save()

    def update_wage(self, wage):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.wage = wage
        job.save()

    def update_city(self, city):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.city = city
        job.save()
