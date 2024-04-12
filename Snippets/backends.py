from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
UserUsers = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserUsers.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserUsers.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserUsers.objects.get(pk=user_id)
        except UserUsers.DoesNotExist:
            return None
