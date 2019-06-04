from .models import User

__all__ = ['UserManager']


class UserManager:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def create(self, profile=None):
        if not profile:
            profile = 1

        User.objects.get_or_create(
            user_id=self.user_id,
            username=self.username,
            profile=profile)

    def update_profile(self, profile):
        user = User.objects.get(user_id=self.user_id)
        user.profile = profile
        user.save()

    def get_user(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            pass
