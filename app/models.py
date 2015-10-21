"""
Definition of models. This is our main model for creating and 
defining our information in the database.
"""

from django.db import models


class RegisterUser(models.Model):
    """ Register User for CryptoStorage """
    email       = models.EmailField(max_length=200, primary_key=True)
    first_name  = models.CharField(max_length=60, null=False, blank=False)
    last_name   = models.CharField(max_length=60, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_update = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        """ To display the email on the template """
        return self.email

class File(models.Model):
    """ The File table to contain all information of user's files """
    file_name  = models.CharField(max_length=200, null=False, blank=False)
    file_hash  = models.CharField(max_length=32, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
    user = models.ForeignKey(RegisterUser)

    def __unicode__(self):
        return self.file_name

class PassUser(models.Model):
    """ Password Table of users """
    pass_hash = models.CharField(max_length=200,null=False, blank=False)
    pass_salt = models.CharField(max_length=200,null=False, blank=False)
    user = models.OneToOneField(RegisterUser)
