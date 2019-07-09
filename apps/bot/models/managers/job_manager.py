from bot.models.tables import Job
from .base_manager import Manager


class JobManager(Manager):

    def create(self, category):
        Job.objects.create(
            user_id=self.user_id, category=category)

    def clean(self):
        Job.objects.filter(user_id=self.user_id, position=None).delete()

    def update_position(self, position):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.position = position
        job.save()

    def update_looking_for(self, looking_for):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.looking_for = looking_for
        job.save()

    def update_wage(self, wage):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.wage = wage
        job.save()

    def update_city(self, city):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        if city == 'Отдалённая работа':
            job.remote = True
        else:
            job.city = city
        job.save()

    def update_experience(self, experience):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.experience = experience
        job.save()

    def update_description(self, description):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.description = description
        job.save()

    def update_write_to_employer(self, write_to_employer):
        job = Job.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        job.write_to_employer = write_to_employer
        job.save()

    def get_vacations(self, params=None):
        if params.city == 'Отдалённая работа':
            job = Job.objects.filter(
                category=params.category,
                position=params.position,
                remote=True
            ).order_by('timestamp')
        elif params.city:
            job = Job.objects.filter(
                category=params.category,
                position=params.position,
                city=params.city
            ).order_by('timestamp')
        else:
            job = Job.objects.filter(
                user_id=self.user_id).order_by('timestamp')
        return job

    def last_job(self):
        job = Job.objects.filter(user_id=self.user_id).order_by(
            'timestamp').reverse().first()
        return job

    def get_vacation_for_id(self, vacation_id):
        job = Job.objects.get(id=vacation_id)
        return job

    def update_vacations(self, vacation_id):
        job = Job.objects.get(id=vacation_id)
        job.is_active = True
        job.save()

    def delete_vacations(self, vacation_id):
        Job.objects.get(id=vacation_id).delete()

    def publish(self):
        resume = Job.objects.filter(
            user_id=self.user_id, publish=False
        ).order_by('timestamp').reverse().first()
        if resume:
            resume.publish = True
            resume.is_active = True
            resume.save()

    def job(self, job_id):
        return Job.objects.get(id=job_id)
