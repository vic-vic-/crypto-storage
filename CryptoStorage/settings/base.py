"""
This module is the base for the settings of our settings app.

"""

#import os

# Special note: It is a good idea NOT to import to settings modules
#               because it may render app useless if load improperly.
# Although in our case it is an exception to handle missing key errors!
from django.core.exceptions import ImproperlyConfigured


# Note: This file env.json has secret variables for Database and SECRET_KEY. 
#       This file is placed outside the root project. It should not be part  
#       of source control for security reasons.

from os import path
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
SECRET_FILE = path.join(path.dirname(path.dirname(path.dirname(
              path.abspath(path.dirname(__file__))))),"env.json")

# to manipulate the json file for secret variables
import json
with open(SECRET_FILE) as sec_f:
    sec_data = json.loads(sec_f.read())

def sec_get(sec_name,sec_data=sec_data):
    """ Attempt to acquire the JSON secrets.
        Thanks to Django Two scoops book for this advise!
    """
    try:
        return sec_data[sec_name]
    except KeyError:
        err_msg = "Environment variable {} not found. Please check".format(sec_name)
        raise ImproperlyConfigured(err_msg)


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Database used for our user data
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     sec_get("DJANGO_DBNAME"),
        'USER':     sec_get("DJANGO_DBU"),
        'PASSWORD': sec_get("DJANGO_DBP"),
        'HOST':     sec_get("DJANGO_DBHOST"),
        'PORT':     sec_get("DJANGO_DBPORT"),
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = sec_get("DJANGO_SKEY")


