# Generated by Django 3.1.4 on 2021-02-06 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_auto_20210206_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
