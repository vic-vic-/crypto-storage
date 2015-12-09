# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_saltrepo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_hash',
        ),
        migrations.AddField(
            model_name='file',
            name='file_hmac',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='file_salt',
            field=models.CharField(default='empty', max_length=16),
            preserve_default=False,
        ),
    ]
