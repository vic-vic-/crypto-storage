"""
Definition of views.
"""
# import our own authentication
from app.userauthbackend import UserAuthBackend

# other necessary dependencies.
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth import login, logout
from app.userauthbackend import UserAuthBackend
from app.forms import RegisterUserAuthenticationForm, RegisterUserForm
from django.contrib.auth.decorators import login_required
from datetime import date

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
                context_instance = RequestContext(request,
                {
                    # pass all required variables to the login verify form
                    'title':'Enter your Password.',
                    'form': authForm,
                    # for the copyright note in the footer
                    'year': date.today().year,
                    'salt'  : userSalt,
                    'email' : email
                })
            )
    return render(
        request,
        'app/loginuser.html',
        context_instance = RequestContext(request,
        {
            'title':'Welcome To CryptoStorage. Please Log In',
            # override the value of form
            'form': authForm,
            # for the copyright note in the footer
            'year': date.today().year
        })
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
    if request.method == 'POST':
        valid_form = authForm.is_valid()
        auth_valid = authForm.authenticate(request)
        # populate fields for form usage
        email = request.POST['email']
        authbackend = UserAuthBackend()
        userSalt = authbackend.get_user_salt(email)
     
        # check if all authentication is ok
        # display form errors if necessary
        #user = authForm.authenticate(request)
        #user = authbackend.get_user(email)
        error = auth_valid['error']
        if auth_valid['error'] == '' or auth_valid['user'] is not None:
                # the generated hash from the client
                #generatedHash = request.POST['hash']

                # check if user is able to login (locked out)
                # if authbackend.confirm_login_allowed(user):
                    # authenticate the client hash to the server's hash
                    # if authbackend.authenticate_hash(email,generatedHash):
            
                #user = authbackend.get_user(email)
                login(request,auth_valid['user'])
                # takes us to the user's home page
                return redirect('/')
        else:
            return render(
                request,
                'app/loginuser.html',
                context_instance = RequestContext(request,
                {
                    'title':'Welcome To CryptoStorage. Please Log In',
                    'error': error,
                    # override the value of form
                    'form': authForm,
                    # for the copyright note in the footer
                    'year': date.today().year
                })
            )
    else:
        return render(
            request,
            'app/loginuser.html',
            context_instance = RequestContext(request,
            {
                'title':'Welcome To CryptoStorage. Please Log In',
                'error': error,
                # override the value of form
                'form': authForm,
                # for the copyright note in the footer
                'year': date.today().year
            })
        )


    return render(
        request, 
        "app/loginverify.html",
         context_instance = RequestContext(request,
        {
            'title':'Enter your Password.',
             # for the copyright note in the footer
            'year': date.today().year,
            'salt'  : userSalt,
            'email' : email,
             'form': authForm
        })
     )

# logs out the user
def logoutuser(request):
    """ logs out the user """
    # ensure that the request is valid, otherwise raise
    assert isinstance(request, HttpRequest)

    logout(request)
    return render(
        request, 
        "app/logoutuser.html",
        context_instance = RequestContext(request,
        {
            'title':'You have successfully logged off.',
            # for the copyright note in the footer
            'year': date.today().year
         })
        )

# this is the home page of the user once logged in
@login_required
def home(request):
    return render(
        request, 
        "app/usermain.html",
        context_instance = RequestContext(request,
        {
            'title':'Home CryptoStorage',
            # for the copyright note in the footer
            'year': date.today().year
         })
        )

# registration form for new users
def register(request):
    return render(
        request, 
        "app/register.html",
        context_instance = RequestContext(request,
        {
            'title':'Registration Form.',
            'form': RegisterUserForm(),
            # for the copyright note in the footer
            'year': date.today().year
         })
        )

