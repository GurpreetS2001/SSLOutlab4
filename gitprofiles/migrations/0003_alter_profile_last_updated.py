# Generated by Django 3.2.6 on 2021-09-19 06:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gitprofiles', '0002_auto_20210916_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
