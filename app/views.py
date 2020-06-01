"""
Definition of views.
"""
# import our own authentication
from app.userauthbackend import UserAuthBackend

# other necessary dependencies.
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login, logout
from app.userauthbackend import UserAuthBackend
from app.forms import RegisterUserAuthenticationForm, RegisterUserForm
from app.models import File
from django.contrib.auth.decorators import login_required
from datetime import date
from os import path
from django.conf import settings
import json
# encdoing for sending file
from django.utils.encoding import smart_str

def loginuser(request):

    """ Renders the user login page(main page)."""

    # ensure that the request is valid, otherwise raise
    assert isinstance(request, HttpRequest)
    # if we go to the main page, we need to ensure
    # we log out the user for security reasons.
    logout(request)
    # override the form object with our custom one
    authbackend = UserAuthBackend()
    authForm = RegisterUserAuthenticationForm()
    # the user has submitted the form.
    if request.method == 'POST':
        email = request.POST['email']
        # verify if user is valid
        user = authbackend.get_user(email)
        userSalt = authbackend.get_user_salt(email)
        if userSalt != '':
            return render(
                request,
                'app/loginverify.html',
                context = 
                {
                    # pass all required variables to the login verify form
                    'title':'Enter your Password.',
                    'form': authForm,
                    # for the copyright note in the footer
                    'year': date.today().year,
                    'salt'  : userSalt,
                    'email' : email
                }
            )
    return render(
        request,
        'app/loginuser.html',
        context = 
        {
            'title':'Welcome To CryptoStorage. Please Log In',
            # override the value of form
            'form': authForm,
            # for the copyright note in the footer
            'year': date.today().year
        }
    )


def loginverify(request):
    """ 
    a client/server handshake page for verifying and 
    authenticating the user.
    """

    # ensure that the request is valid, otherwise raise
    assert isinstance(request, HttpRequest)
    
    # create the authentication form object
    authForm = RegisterUserAuthenticationForm(request.POST or None)
    # initialize fields for form
    userSalt = ''
    email = ''
    error = ''
    file_security_properties = ''
    if request.method == 'POST':
        valid_form = authForm.is_valid()
        auth_valid = authForm.authenticate(request)
        # populate fields for form usage
        email = request.POST['email']
        authbackend = UserAuthBackend()
        userSalt = authbackend.get_user_salt(email)
     
        # check if all authentication is ok
        # display form errors if necessary
        error = auth_valid['error']

        # authenticate if any error or user was not found
        if auth_valid['error'] == '' or auth_valid['user'] is not None:
            login(request,auth_valid['user'])
            return render(
                request, 
                "app/usermain.html",
                context = 
                {
                    'title':'Home CryptoStorage',
                    'user': request.user,
                    # for the copyright note in the footer
                    'year': date.today().year
                    }
                )
        else:
            return render(
                request,
                'app/loginuser.html',
                context = 
                {
                    'title':'Welcome To CryptoStorage. Please Log In',
                    'error': error,
                    # override the value of form
                    'form': authForm,
                    # for the copyright note in the footer
                    'year': date.today().year
                }
            )
    else:
        return render(
            request,
            'app/loginuser.html',
            context = 
            {
                'title':'Welcome To CryptoStorage. Please Log In',
                'error': error,
                # override the value of form
                'form': authForm,
                # for the copyright note in the footer
                'year': date.today().year
            }
        )


    return render(
        request, 
        "app/loginverify.html",
         context = 
        {
            'title':'Enter your Password.',
             # for the copyright note in the footer
            'year': date.today().year,
            'salt'  : userSalt,
            'email' : email,
             'form': authForm
        }
     )


def logoutuser(request):
    """ logs out the user """
    # ensure that the request is valid, otherwise raise
    assert isinstance(request, HttpRequest)

    logout(request)
    return render(
        request, 
        "app/logoutuser.html",
        context = 
        {
            'title':'You have successfully logged off.',
            # for the copyright note in the footer
            'year': date.today().year
         }
        )


@login_required
def home(request):
    """
    this is the home page of the user once logged in
    """
    return render(
        request, 
        "app/usermain.html",
        context = 
        {
            'title':'Home CryptoStorage',
            # for the copyright note in the footer
            'year': date.today().year
         }
        )


def register(request):
    """
    registration form for new users
    """
    if request.method == 'POST':
        #TODO do more request checking
        email = request.POST['email']
        # verify if user is valid
        form = RegisterUserForm(request.POST)
        # create the authentication form object
        authForm = RegisterUserAuthenticationForm(request.POST or None)
        valid = form.is_valid()
        if form.is_valid():
            form.save()
            return render(
                request,
                'app/loginuser.html',
                context = 
                {
                    'title':'Welcome To CryptoStorage. Please Log In',
                    'message': 'Registration successful',
                    # override the value of form
                    'form': authForm,
                    # for the copyright note in the footer
                    'year': date.today().year
                }
            )
    return render(
        request, 
        "app/register.html",
        context =
        {
            'title':'Registration Form.',
            'form': RegisterUserForm(),
            # for the copyright note in the footer
            'year': date.today().year
         }
        )

@login_required
def file_process(request):
    """
    processes the file cipher text and details
    to store in the database/user directory
    """

    if request.method == 'POST':
        # flag to return if everything was ok
        success = False
        ## obtain all fields from post if available
        file_command = request.POST['file_command']



        # check what operation we need to perform
        if file_command == 'set':
            # get the file security properties to store them in server
            file_security_properties = request.POST['file_security_properties']

            # parse the received data salt$file_name
            fsp_parsed = file_security_properties.split('$')
            # get encrypted file data
            encrypted_data = request.POST['file_data']
        
            # encrypted settings from file encryption
            encrypt_settings = request.POST['encrypt_settings']
            # create file object from file model
            file_object_exists = ""
            try:

                file_object_exists = File.objects.get(
                                file_name=fsp_parsed[1],
                                user=request.user
                                )
            except:
                print("Error file doesn't exist.")
                pass
            
            # insert the updated fields accordingly
            if file_object_exists:
                file_object_exists.file_salt=fsp_parsed[0]
                file_object_exists.file_hmac=encrypt_settings
                file_object_exists.user=request.user
                file_object_exists.save()
            else:
                File.objects.create(
                                file_name=fsp_parsed[1],
                                file_salt=fsp_parsed[0],
                                file_hmac=encrypt_settings,
                                user=request.user
                                )
            # remove the file ext
            file_name_no_ext = path.splitext(fsp_parsed[1])[0]

            # create the file and write the encrypted info (read and write)
            # store the file in the server
            full_filename_path = path.join(settings.PROJECT_ROOT,path.join("tmp",file_name_no_ext))
            file_create = open(full_filename_path,'w+')
            file_create.write(encrypted_data)

            # save file properties to the database
            file_create.close()
            server_response = json.dumps({ 'response': 'OK', 'file_name': fsp_parsed[1]})
            # return the file name to the user
            return HttpResponse(server_response, content_type="application/json")

        elif file_command == 'get':
            # get file data for the user
                       
            # remove the file ext
            file_name = request.POST['file_name']
            file_name_no_ext = path.splitext(file_name)[0]
            # get the encrypt_settings and salt based on file
            file_get = File.objects.get(file_name=file_name, user=request.user)
            encrypt_settings = file_get.file_hmac
            file_salt = file_get.file_salt

            # read the encrypted data
            full_filename_path = path.join(settings.PROJECT_ROOT,path.join("tmp",file_name_no_ext))
            file_get = open(full_filename_path,'r')
            # read the encrypted data
            encrypted_data = file_get.read()
            file_get.close()

            # compose the message to send
            # TODO: incorporate file download option
            # to client location
            server_response = json.dumps({ 
                                            'response': 'OK', 
                                            'encrypt_settings': encrypt_settings,
                                            'file_salt': file_salt,
                                            'encrypted_data': encrypted_data
                                        })
            # return the file name to the user
            return HttpResponse(server_response, content_type="application/json")

        else:
            # was not able to get the command. Respond with server error
            return HttpResponse("SERVER ERROR",content_type="text/plain")


