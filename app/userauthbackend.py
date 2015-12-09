"""
A custom authentication backend to override all defaults
for security reasons. 
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import check_password
from .models import RegisterUser
from .passwordengine import *

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
            user = self.get_user(email=email)
            # authenticate if password match
            if user.check_password(password):
                return user
            else:
                return None
        except:
            return None

    def authenticate_hash(self, email=None, generatedHash=None):
        """
        Authenticate user based on the email and hash generated from the client side.
        return true if database hash matches the generated hash from client.
        """
        # need to get user object
        user = self.get_user(email=email)
        if user is not None:
            dbHash = self.get_password_element(email,'hash')
            if generatedHash == dbHash:
                # reset the login attempts if successful
                user.login_attempts = 0
                user.save()
                return True
            else:
                # increment the attempts being used for authenticating this 
                # particular user to prevent brute force attacks.
                # if user has exceeded the max attempts of 3, then lock the user.
                if user.login_attempts >= 3:
                    user.is_active = False
                    user.save()
                    return False
                user.login_attempts += 1
                user.save()
                return False
        else:
            return False
            
    def get_user(self, email):
        """
        One of two required functions for defining a custom auth backend.
        For obtaining a user object if it exists.
        """
        try:
            return RegisterUser.objects.get(email=email)
        except:
            return None

    def get_user_salt(self, email):
        """
        return a salt from the database based on email. Otherwise send a random
        hash and keep it for that username (for security reasons).
        """
        
        salt = self.get_password_element(email,'salt')
        # if salt returns empty then we must insert one to table
        pe = PasswordEngine()
        if salt == '':
            salt = pe.create_salt(email)
        return salt

    def confirm_login_allowed(self, user):
        """ 
        checks if user can be allowed to log in 
        returns true if active, false otherwise.
        """
        # if the user has been disabled due to incorrect
        # password retries or other.
        if not user.is_active:
            return False;  
        return True  
    
      
    def get_password_element(self, email, element) :
        """
        Gets the element('salt', 'hash') value based on the user's email

        returns the desired password's element value
        """
        # variable to store the element's value
        elementValue = '';
        try:
            user = RegisterUser.objects.get(email=email)
            # lets check if user exists
            if user is not None:
                # django password pbkdf2 object structure is type$iterations$salt$hash
                passObj = user.password.split('$')
                if element == 'salt':
                    elementValue = passObj[2]
                elif element == 'hash':
                    elementValue = passObj[3]
            else:
                elementValue = ''
        except:
            elementValue = ''

        return elementValue   