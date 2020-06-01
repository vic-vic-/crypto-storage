# Generated by Django 3.0.6 on 2020-06-01 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200531_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='passuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registeruserprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
