# Generated by Django 5.0.6 on 2024-06-16 21:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_studentgroup_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL, verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user_phone',
            field=models.CharField(blank=True, max_length=25, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, verbose_name='Номер телефона'),
        ),
    ]
