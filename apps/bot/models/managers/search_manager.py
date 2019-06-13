from bot.models.tables import Search

__all__ = ('SearchManager',)


class SearchManager:
    def __init__(self, user_id):
        self.user_id = user_id

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
