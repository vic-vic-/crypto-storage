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
    authForm = RegisterUserAuthenticationForm()
    authbackend = UserAuthBackend()
    # the user has submitted the form.
    if request.method == 'POST':
        email = request.POST['email']
        # verify if user is valid
        user = authbackend.get_user(email)
        if user is not None:
            if authbackend.authenticate(email,password=request.POST['password']) is not None:
                if authForm.confirm_login_allowed(user):
                    login(request,user)
                    # takes us to the user's home page
                    return redirect('/')

    # TODO: need to render the loginVerify
    #       so the server can send the salt for computing
    #       the password on client side.
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
    return render(
        request, 
        "app/loginverify.html",
         context_instance = RequestContext(request,
        {
            'title':'Enter your Password.',
             # for the copyright note in the footer
            'year': date.today().year
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

