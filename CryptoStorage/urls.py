"""
Definition of urls for CryptoStorage.
"""

from datetime import datetime
from django.conf.urls import patterns, url
#from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # main page url
    url(r'^$', 'app.views.home', name='home'),

    # registration redirection
    url(r'^register/$', 'app.views.register', name='register'),

    # the client/server verification for entering password.
    url(r'^verify/$', 'app.views.loginverify', name='loginverify'),

    # we use django's internal login template for security purposes
    # with our formatted loginuser.html
    url(r'^login/$', 
        'app.views.loginuser',
        #{
        #    'template_name': 'app/loginuser.html',
        #},
        name='login'),
    # we use django's internal logout template for security purposes
    # with only to a rediretion to logout page
    url(r'^logout/$', 'app.views.logoutuser',
        #'django.contrib.auth.views.logout',
        #{
            #'next_page': '/',
        #    'template_name': 'app/logoutuser.html',
        #},
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # DO NOT ENABLE IN PRODUCTION. ADMIN FOR LOCAL ADMINISTRATION!!!
    url(r'^admin/', include(admin.site.urls)),
)
