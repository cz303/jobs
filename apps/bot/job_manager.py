from .models import Job

__all__ = ('JobManager',)


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

    def update_experience(self, experience):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.experience = experience
        job.save()

    def update_description(self, description):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.description = description
        job.save()

    def update_write_to_employer(self, write_to_employer):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        job.write_to_employer = write_to_employer
        job.save()
