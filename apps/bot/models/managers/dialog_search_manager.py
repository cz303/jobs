from bot.models.tables import Searching
from .base_manager import Manager


class DialogSearchManager(Manager):

    def start(self):
        Searching.objects.create(user_id=self.user_id, start=True)

    def update_city(self):
        search = Searching.objects.filter(user_id=self.user_id).first()
        search.start = False
        search.city = True
        search.save()

    def update_category(self):
        search = Searching.objects.filter(user_id=self.user_id).first()
        search.city = False
        search.category = True
        search.save()

    def update_position(self):
        search = Searching.objects.filter(user_id=self.user_id).first()
        search.category = False
        search.position = True
        search.save()

    def clean(self):
        Searching.objects.filter(user_id=self.user_id).delete()

    def check_start(self):
        search = Searching.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not search:
            return False
        else:
            return search.start

    def check_city(self):
        search = Searching.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not search:
            return False
        else:
            return search.city

    def check_category(self):
        search = Searching.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not search:
            return False
        else:
            return search.category

    def check_position(self):
        search = Searching.objects.filter(
            user_id=self.user_id).order_by('-created').first()
        if not search:
            return False
        else:
            return search.position
