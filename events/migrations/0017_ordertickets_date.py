# Generated by Django 3.0.8 on 2020-07-30 17:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20200727_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertickets',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 30, 17, 13, 47, 800096, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
