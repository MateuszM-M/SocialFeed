# Generated by Django 3.1.4 on 2021-02-01 21:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accounts', '0009_auto_20210201_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accepted', 'accepted')], default='send', max_length=8),
        ),
    ]
