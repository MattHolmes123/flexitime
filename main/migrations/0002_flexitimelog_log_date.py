# Generated by Django 2.2.7 on 2019-12-11 20:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flexitimelog',
            name='log_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
