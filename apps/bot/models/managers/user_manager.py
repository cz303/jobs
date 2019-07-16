from bot.models.tables import User

__all__ = ('UserManager',)


class UserManager:
    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username

    def create(self, profile=None):
        if not profile:
            profile = 1

        User.objects.create(
            user_id=self.user_id,
            profile=profile,
            username=self.username
        )

    def update_profile(self, profile):
        user = User.objects.get(user_id=self.user_id)
        user.profile = profile
        user.save()

    def get_user(self):
        return User.objects.filter(user_id=self.user_id)

    def set_phone(self, phone):
        user = User.objects.get(user_id=self.user_id)
        user.phone = phone
        user.save()

    def get_score(self):
        user = User.objects.get(user_id=self.user_id)
        return user.credit

    def update_credit(self, credit):
        user = User.objects.get(user_id=self.user_id)
        user.credit = credit
        user.save()

    def free_send(self):
        user = User.objects.get(id=self.user_id)
        user.free_send = True
        user.save()
