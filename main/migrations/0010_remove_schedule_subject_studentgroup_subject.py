# Generated by Django 5.0.6 on 2024-06-07 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_teacher_groups_studentgroup_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='subject',
        ),
        migrations.AddField(
            model_name='studentgroup',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_groups', to='main.subject', verbose_name='Предмет'),
            preserve_default=False,
        ),
    ]
