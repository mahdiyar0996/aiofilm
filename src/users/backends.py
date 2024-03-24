from django.contrib.auth.hashers import check_password
from django.db.models import Q
from .models import User
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class EmailUsernameAuthentication(ModelBackend):

    def authenticate(self, request, email=None, username=None, password=None):
        if (username is None and password is None) or (email is None and password is None):
            return None
        try:
            user = User.objects.get(Q(username__exact=username) |
                                    Q(email__exact=email)
                                    )
        except User.DoesNotExist:
            return None
        if user and check_password(password, user.password):
            return user
        return None


