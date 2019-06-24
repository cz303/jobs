from bot.models.tables import Statistics
from .base_manager import Manager


class StatisticsManager(Manager):

    def create(self):
        Statistics.objects.create(
            user_id=self.user_id,
            count=0,
            sent_to_users='',
            price=0,
            funds_spent=0,
            free_send=10
        )

    def save(self, count, sent_to_users, price, funds_spent, free_send):
        Statistics.objects.update(
            user_id=self.user_id,
            count=count,
            sent_to_users=sent_to_users,
            price=price,
            funds_spent=funds_spent,
            free_send=free_send
        )

    def free_send(self):
        stat = Statistics.objects.get(user_id=self.user_id)
        return stat.free_send

    def save_free_send(self, count):
        stat = Statistics.objects.get(user_id=self.user_id)
        stat.free_send = count if count > 0 else 0
        stat.save()

    def get(self):
        return Statistics.objects.get(user_id=self.user_id)
