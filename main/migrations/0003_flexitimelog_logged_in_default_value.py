# Generated by Django 2.2.7 on 2019-12-29 10:59

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_flexitimelog_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexitimelog',
            name='logged_in',
            field=models.TimeField(default=main.models.time_now),
        ),
    ]