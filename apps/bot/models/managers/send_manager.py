from .base_manager import Manager
from bot.models.tables import SendDialog


class SendManager(Manager):

    def create(self, job_id, resumes_ids):
        return SendDialog.objects.create(
            user_id=self.user_id,
            checker_start=True,
            candidates=resumes_ids,
            resume_id=job_id)

    def checker(self):
        check = SendDialog.objects.filter(user_id=self.user_id).last()

        if check:
            return check.checker_start

    def candidates(self):
        can = SendDialog.objects.get(user_id=self.user_id)
        return can.candidates

    @classmethod
    def delete(cls, user_id):
        try:
            SendDialog.objects.get(user_id=user_id).delete()
        except SendDialog.DoesNotExist as error:
            print(str(error))