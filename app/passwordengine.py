"""
This class is used for password management. It creates a salt for new users,
gets salt from register users, and helps maintain a unique salt in the
database.

"""

# lib used for generating passwords
from os import urandom
import django.contrib.auth
from random import randint

# import for accessing db
import app.models as db

class PasswordEngine(object):
    """Password Manager to help create, get, and maintain unique passwords in DB
       for registered or new users."""

    # TODO: Finish implementation 
    def create_salt(self):
        """ 
        Creates salt for use when hashing password for user.
        Stores it in a table to avoid reuse. 

        returns a random 128 bit salt.
        """
        # attempt max 10 tries for generating salt if we hit the
        # same salt in the file
        tries = 10
        salt = ""
        valid = False
        
        while tries > 0:
            salt = calculate_salt()
            
            # check the file if salt exists, if not, save it into file.
            if(check_salt_infile("saltTable.txt",salt) == False):
                if(insert_salt_infile("saltTable.txt",salt)):
                    valid = True
                    break
            tries -= 1
        return salt
        # check if the salt exists
        # check if the salt exists in a file
        # saltFile = open("salt_table.txt", "rw+")
        # for line in saltFile.readlines():
            #if( salt == line)
            
    def _calculate_salt(self):
        """
        Formulates the 128 bit salt

        returns the salt.
        """
        # we will pick a random number from 2^0 to 2^10 for iterations
        counter = randint(1,1024)
        salt = ""
        
        # perforom calculation of salt.
        for i in range(0, counter):
            # random 128 bits for salt usage
            salt = urandom(16)
        return salt

    def _check_salt_infile(self,file,salt):
        """ 
        Checks the salt file if the salt exists. This helps prevent
        reuse of the salt for users.

        returns true if 'salt' was found from 'file'.
        """
        foundSalt = False
        try:
            # open file with only read
            saltFile = open(file,"r")
            for line in saltFile.readlines():
                if (salt == line):
                    foundSalt = True
            saltFile.close()
        except:
            raise ValueError("An error occured checking salt from file table.")
            
        return foundSalt

    def __insert_salt_infile(db,salt):
        """ 
        Inserts the salt into the file.
        returns true if 'salt' was found from 'file'.
        """
        insertSuccess = False
        try:
            # if(file==None | salt == None):
                # raise ValueError("Invalid file or salt parameter")
            # open file with only read
            saltFile = open(db,"rw+")
            saltFile.write(salt + "\r\n")
            saltFile.close()
            insertSuccess = True
        except:
            raise ValueError('An error occured inserting salt to file table.')
        return insertSuccess

    def get_hash(self, username) :
        """
        Gets the hash value from the specified user. 

        returns hash of user.
        """
        
        pass