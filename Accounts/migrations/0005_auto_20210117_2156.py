# Generated by Django 3.1.4 on 2021-01-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_auto_20210117_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other'), ('X', 'Do not want to specify')], default='X', max_length=22),
        ),
    ]
