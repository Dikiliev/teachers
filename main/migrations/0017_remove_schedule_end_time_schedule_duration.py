# Generated by Django 5.0.6 on 2024-06-17 22:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_appointment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='end_time',
        ),
        migrations.AddField(
            model_name='schedule',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=7200), verbose_name='Длительность'),
        ),
    ]
