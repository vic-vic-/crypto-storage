"""
This module is for administration only through the admin
site.
"""

# import the administration class and our custom models
# for management.
from django.contrib import admin
from .models import RegisterUser, File, PassUser, SaltRepo

# These are classes defined in our models module (see models.py)
# The admin to this site has total control over these tables 
# of the database. Although this is ONLY ran through local
# settings(development PC) and not through production settings.
# (the Internet).
class RegisterUserAdmin(admin.ModelAdmin):
    class Meta:
        model = RegisterUser

admin.site.register(RegisterUser, RegisterUserAdmin)

class FileAdmin(admin.ModelAdmin):
    class Meta:
        model = File

admin.site.register(File, FileAdmin)

class PassUserAdmin(admin.ModelAdmin):
    class Meta:
        model = PassUser

admin.site.register(PassUser, PassUserAdmin)

class SaltRepoAdmin(admin.ModelAdmin):
    class Meta:
        model = SaltRepo

admin.site.register(SaltRepo, SaltRepoAdmin)