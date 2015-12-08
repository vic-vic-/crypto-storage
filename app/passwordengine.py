"""
This class is used for password management. It creates a salt for new users,
gets salt from register users, and helps maintain a unique salt in the
database.

"""

# lib used for generating passwords
from os import urandom
import django.contrib.auth
from random import randint
from .models import RegisterUser, SaltRepo
from django.contrib.auth import hashers

class PasswordEngine(object):
    """
    This class is used for password management. It creates a salt for new users,
    gets salt from register users, and helps maintain a unique salt in the
    database.
    """

    def create_salt(self, email):
        """ 
        Creates salt for use when hashing password for user.
        Stores it in a table to avoid reuse. 

        returns a random 128 bit salt.
        """
        # attempt max 10 tries for generating salt if we hit the
        # same salt in the repo
        tries = 10
        salt = ""
        valid = False
        # determine if the user exists in the repo then return salt
        user = self._get_user(email)
        if user is not None:
            return user.salt

        while tries > 0:
            salt = self._calculate_salt()
            
            # check the repo if salt exists, if not, save it into repo.
            if(self._check_salt_repo(salt) == False):
                if(self._insert_salt_repo(email=email, salt=salt)):
                    valid = True
                    break
            tries -= 1
        return salt
            
    def _calculate_salt(self):
        """
        Formulates the 128 bit salt using django's default pbkdf2 salt generator

        returns the salt.
        """
        # use the internal django api to generate salt
        saltgen = hashers.BasePasswordHasher()
        return saltgen.salt()

    def _get_user(self,email):
        """
        Check if the user exists in this repo
        """

        user = SaltRepo.objects.get(email=email)
        if user is not None:
            return user
        else:
            return False
            

    def _check_salt_repo(self,salt):
        """ 
        Checks the salt repo if the salt exists. This helps prevent
        reuse of the salt for users.

        returns true if 'salt' was found from 'repo'.
        """
        foundSalt = False
        try:
            # check to see if salt exists
            salt_repo = SaltRepo.objects.get(salt=salt)
            if salt_repo is not None:
                foundSalt = True
        except:
            return foundSalt
            
        return foundSalt

    def _insert_salt_repo(self, email,salt):
        """ 
        Inserts the salt into the repo.

        returns true if 'salt' was found from 'repo'.
        """
        insertSuccess = False
        try:
            salt_repo = SaltRepo(email=email, salt=salt)
            salt_repo.save()
            insertSuccess = True
        except:
            return insertSuccess
        return insertSuccess

        

