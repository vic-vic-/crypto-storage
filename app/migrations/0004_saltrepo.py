# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151206_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaltRepo',
            fields=[
                ('email', models.EmailField(max_length=200, unique=True, serialize=False, primary_key=True, db_index=True)),
                ('salt', models.CharField(max_length=16)),
            ],
        ),
    ]
