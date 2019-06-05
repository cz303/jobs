from .models import User
from django.db.utils import IntegrityError

__all__ = ['UserManager']


class UserManager:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def create(self, profile=1):
        try:
            User.objects.create(
                user_id=self.user_id,
                username=self.username,
                profile=profile)
        except IntegrityError as error:
            print(f'There is such := {error}')

    def update_profile(self, profile):
        user = User.objects.get(user_id=self.user_id)
        user.profile = profile
        user.save()

    def get_user(self):
        try:
            return User.objects.get(user_id=self.user_id)
        except User.DoesNotExist:
            pass
