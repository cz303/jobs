from bot.models.tables import Search
from .base_manager import Manager


class SearchManager(Manager):

    def create_search(self, city):
        return Search.objects.create(user_id=self.user_id, city=city)

    def update_category(self, category):
        search = Search.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        search.category = category
        search.save()

    def update_position(self, position):
        search = Search.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
        search.position = position
        search.save()

    def clean(self):
        Search.objects.filter(user_id=self.user_id).delete()

    def get(self):
        return Search.objects.filter(
            user_id=self.user_id).order_by('timestamp').reverse().first()
