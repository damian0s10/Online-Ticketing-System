# Generated by Django 3.0.8 on 2020-08-02 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20200731_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]