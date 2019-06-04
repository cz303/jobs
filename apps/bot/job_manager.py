from .models import Job

__all__ = ['JobManager']


class JobManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, category):
        Job.objects.get_or_create(
            user_id=self.user_id, category=category)

    def update_position(self, position):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('created').first()
        job.position = position
        job.save()
