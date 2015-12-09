"""
Definition of models. This is our main model for creating and 
defining our information in the database.
Our main reference:
https://docs.djangoproject.com
"""

# All the necessary classes used:
from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class RegisterManager(BaseUserManager) :
    """
    This class manages the user since we need to take care of
    custom fields defined based on password and username requirements.
    """
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates a generic user for accessing our application.
        No Admin priviliges.
        """
        if not email:
            raise ValueError('Invalid email. Email required.')
        # user custom fields
        # password is stored in pbkdf2 since we are receiving
        # the hash from the client side
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        
        user.set_password(password)
        # no admin priviliges
        user.is_admin = False
        #user.is_staff = False
        user.is_active = True
        #user.is_superuser = False
        user.save(using = self._db)
        
        # imported inside function to prevent cyclic import
        from .userauthbackend import UserAuthBackend
        # since user exists we can get the salt
        # doing authentication for salt usage
        salt_get = UserAuthBackend()
        salt = salt_get.get_password_element(email,'salt')
       
        # lets store email and salt in the availability salt table
        salt_repo = SaltRepo(email=email, salt=salt)
        salt_repo.save()

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email=email,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        #user.is_staff = True
        user.is_active = True
        #user.is_superuser = True
        user.save(using = self._db)
        return user

class RegisterUser(AbstractBaseUser):
    """ Registers Users for CryptoStorage """
    email       = models.EmailField(max_length=200, 
                                    primary_key=True, 
                                    unique=True, 
                                    db_index=True)
    first_name     = models.CharField(max_length=60, null=False, blank=False)
    last_name      = models.CharField(max_length=60, null=False, blank=False)
    date_joined    = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_update    = models.DateTimeField(auto_now_add=False, auto_now=True)
    login_attempts = models.IntegerField(default=0,null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # required attribute for login() in views
    backend = 'app.userauthbackend.UserAuthBackend'

    # must username as email due to custom user object
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = RegisterManager()

    def get_full_name(self):
        """return main username => email"""
        return self.email

    def get_short_name(self):
        """return main username => email"""
        return self.email

    #def check_password(self, raw_password):
        #return super(RegisterUser, self).check_password(raw_password)

    def has_perm(self, perm, obj=None):
        """User has specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """User permission to view app_label"""
        return True

    @property
    def is_staff(self):
        """Idenfy if user is an administrator"""
        return self.is_admin

    def __unicode__(self):
        """ To display the email on the template """
        return self.email

class File(models.Model):
    """ The File table to contain all information of user's files """
    file_name  = models.CharField(max_length=200, null=False, blank=False, primary_key=True)
    file_hmac  = models.CharField(max_length=200, null=False, blank=False)
    file_salt  = models.CharField(max_length=16, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
    user = models.ForeignKey(RegisterUser)

    def __unicode__(self):
        return self.file_name

class PassUser(models.Model):
    """ Password Table of users """
    pass_hash = models.CharField(max_length=64,null=False, blank=False)
    pass_salt = models.CharField(max_length=16,null=False, blank=False)
    user = models.OneToOneField(RegisterUser)

    def __unicode__(self):
        return self.user

class SaltRepo(models.Model):
    """ 
    Salt table for availability of salts. Registered and unregistered users
    """
    email       = models.EmailField(max_length=200, 
                                    primary_key=True, 
                                    unique=True, 
                                    db_index=True)
    salt = models.CharField(max_length=16,null=False, blank=False)

    def __unicode__(self):
        return self.email

class RegisterUserProfile(models.Model):
    """Creates profiles for the users"""
    user = models.ForeignKey(RegisterUser)
    url = models.URLField('profile', blank=True)