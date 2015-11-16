"""
Form definitions for utilizing them when calling them from
the html templates.
"""

from django import forms
from app.models import RegisterUser
from django.contrib.auth.forms import (AuthenticationForm, 
                                       UserCreationForm)
#from django.utils.translation import ugettext_lazy as _
# TODO: finish and integrate the registration

class RegisterUserAuthenticationForm(AuthenticationForm):
    """ the user login authentication form """
    # form fields intialize
    email = forms.EmailField(label='Email Address', 
                             max_length=50)
    password = forms.CharField(label='Passsword', 
                               max_length=50,
                               widget=forms.widgets.PasswordInput)
    
    class Meta:
        #model = RegisterUser
        fields = ['email', 'password']

    def confirm_login_allowed(self, user):
        """ checks if user can be allowed to log in"""
        # if the user has been disabled due to incorrect
        # password retries or other.
        if not user.is_active:
            raise forms.ValidationError("The account has been disabled. "+
                "Please contact customer service.")    
        return True                  

class RegisterUserForm(UserCreationForm):
    """ The registration form used for new users. """
    # all fields defined
    email = forms.EmailField(label='Email Address', max_length=50)
    first_name = forms.CharField(label='First Name', max_length=25)
    last_name = forms.CharField(label='Last Name', max_length=25)
    password1 = forms.CharField(label='Passsword', max_length=50)
    password2 = forms.CharField(label='Re-enter Password', max_length=50)
    
    class Meta:
        model = RegisterUser
        fields = ['email', 'first_name', 'last_name', 'password1','password2']

    def clean_email(self):
        """ checks if email is available. """
        email = self.cleaned_data["email"]
        try:
            user = RegisterUser.objects.get(email=email)
            raise forms.ValidationError("Email exists already. Use another email.")
        except RegisterUser.DoesNotExist:
            return email

    def save(self, commit=True):
        """ registers the user. """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user
