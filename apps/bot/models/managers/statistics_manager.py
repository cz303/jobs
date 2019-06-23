from bot.models.tables import Statistics
from .base_manager import Manager


class StatisticsManager(Manager):

    def save(self, count, sent, price, funds_spent):
        Statistics.objects.create(
            user_id=self.user_id,
            count=count,
            sent=sent,
            price=price,
            funds_spent=funds_spent
        )
