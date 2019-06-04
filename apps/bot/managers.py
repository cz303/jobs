from .models import User
from django.db.utils import IntegrityError


class UserManager:
    @classmethod
    def get_or_create(cls, user_id, profile, username):
        try:
            User.objects.create(
                user_id=user_id,
                profile=profile,
                username=username
            )
        except IntegrityError:
            return User.objects.get(user_id=user_id)

    @classmethod
    def update_user(cls, user_id, username, profile):
        return User.objects.update(user_id=user_id,
                                   username=username,
                                   profile=profile)
