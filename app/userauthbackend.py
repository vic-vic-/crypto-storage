"""
A custom authentication backend to override all defaults
for security reasons. 
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import check_password
from .models import RegisterUser

class UserAuthBackend(object):
    """
    Custom Authentication backend for CryptoStorage use.
    """
    def authenticate(self, email=None, password=None):
        """
        One of two required functions for defining a custom auth backend.
        For authenticating user credentials.
        """
        try:
            user = RegisterUser.objects.get(email=email)
            # authenticate if password match
            if user.check_password(password):
                return user
            else:
                return None
        except RegisterUser.DoesNotExist:
            return None

    def get_user(self, email):
        """
        One of two required functions for defining a custom auth backend.
        For obtaining a user object if it exists.
        """
        try:
            return get_user_model().objects.get(pk=email)
        except RegisterUser.DoesNotExist:
            return None