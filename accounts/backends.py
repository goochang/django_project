from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        try:
            user = user_model.objects.get(username=username)
            print("authenticate", password)
            if user.check_password(password):  # check valid password
                return user  # return user to be authenticate
            # else:
            #     print("check false")
            #     return user
        except user_model.DoesNotExist:  # no matching user exists
            print("except")
            return None
