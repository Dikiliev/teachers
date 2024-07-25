# Generated by Django 5.0.6 on 2024-07-25 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_testresult_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Создано'), ('ACCEPTED', 'Принято'), ('REJECTED', 'Отклонено')], default='CREATED', max_length=10, verbose_name='Статус'),
        ),
    ]
