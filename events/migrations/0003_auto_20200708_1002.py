# Generated by Django 3.0.8 on 2020-07-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200708_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='categories',
            field=models.CharField(choices=[('sport', 'sport'), ('concerts', 'concerts'), ('thearte', 'thearte'), ('stand-up', 'stand-up'), ('for-children', 'for-children'), ('cinema', 'cinema'), ('others', 'others')], max_length=20),
        ),
    ]
