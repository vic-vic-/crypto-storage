# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_registeruser_loginattempts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registeruser',
            old_name='loginAttempts',
            new_name='login_attempts',
        ),
    ]
