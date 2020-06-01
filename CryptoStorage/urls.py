"""
Definition of urls for CryptoStorage.
"""

from datetime import datetime
from django.urls import path
#from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()
from app import views

urlpatterns = [
    # main page url
    path('', views.home, name='home'),

    # registration redirection
    path('register/', views.register, name='register'),

    # the client/server verification for entering password.
    path('verify/', views.loginverify, name='loginverify'),

    # we use django's internal login template for security purposes
    # with our formatted loginuser.html
    path('login/', 
        views.loginuser,
        #{
        #    'template_name': 'app/loginuser.html',
        #},
        name='login'),
    # we use django's internal logout template for security purposes
    # with only to a rediretion to logout page
    path('logout/', views.logoutuser,
        #'django.contrib.auth.views.logout',
        #{
            #'next_page': '/',
        #    'template_name': 'app/logoutuser.html',
        #},
        name='logout'),
    # request for processing the file to the server and getting
    # file from the server
    path('file_process/', views.file_process, name='file_process'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # DO NOT ENABLE IN PRODUCTION. ADMIN FOR LOCAL ADMINISTRATION!!!
    path('admin/', admin.site.urls),
]
