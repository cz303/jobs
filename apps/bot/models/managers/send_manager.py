from .base_manager import Manager
from bot.models.tables import SendDialog


class SendManager(Manager):

    def create(self, job_id, candidates):
        return SendDialog.objects.create(
            user_id=self.user_id,
            checker_start=True,
            candidates=candidates,
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
        SendDialog.objects.filter(user_id=user_id).delete()

    def sender(self):
        try:
            return SendDialog.objects.get(user_id=self.user_id)
        except SendDialog.DoesNotExist as error:
            print(str(error))

    def count(self, count):
        can = SendDialog.objects.get(user_id=self.user_id)
        can.count = count
        can.save()
