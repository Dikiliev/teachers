# Generated by Django 5.0.6 on 2024-06-01 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_subject_alter_user_avatar_alter_user_phone_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название группы')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Аватарка'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Понедельник'), (2, 'Вторник'), (3, 'Среда'), (4, 'Четверг'), (5, 'Пятница'), (6, 'Суббота'), (7, 'Воскресенье')], verbose_name='День недели')),
                ('start_time', models.TimeField(verbose_name='Время начала')),
                ('end_time', models.TimeField(verbose_name='Время окончания')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='main.subject', verbose_name='Предмет')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='main.teacher', verbose_name='Преподаватель')),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='main.studentgroup', verbose_name='Группа студентов')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='groups',
            field=models.ManyToManyField(related_name='teachers', to='main.studentgroup', verbose_name='Группы студентов'),
        ),
    ]
