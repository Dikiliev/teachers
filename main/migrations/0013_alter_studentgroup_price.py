# Generated by Django 5.0.6 on 2024-06-13 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_appointment_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgroup',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена'),
        ),
    ]
