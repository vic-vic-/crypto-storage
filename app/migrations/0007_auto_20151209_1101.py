# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_registeruserprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='id',
        ),
        migrations.AlterField(
            model_name='file',
            name='file_name',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
        ),
    ]
