# Generated by Django 3.0.4 on 2020-03-11 23:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('kitup', '0002_auto_20200311_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='joined_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 11, 23, 9, 44, 176825, tzinfo=utc)),
        ),
    ]
