# Generated by Django 3.0.8 on 2020-07-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_ordertickets_braintree_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
