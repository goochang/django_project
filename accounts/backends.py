from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        user_model = get_user_model()
        if user_id is None:
            user_id = kwargs.get(user_model.USERNAME_FIELD)
        try:
            user = user_model.objects.get(user_id=user_id)
            print("authenticate", password)
            if user.check_password(password):  # check valid password
                return user  # return user to be authenticate
        except user_model.DoesNotExist:  # no matching user exists
            print("except 1")
            return None
