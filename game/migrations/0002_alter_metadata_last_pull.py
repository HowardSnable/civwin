# Generated by Django 3.2.6 on 2021-11-10 08:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadata',
            name='last_pull',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 10, 9, 31, 20, 935700)),
        ),
    ]