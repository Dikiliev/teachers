# Generated by Django 5.0.6 on 2024-06-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_teacher_subjects_teachersubject'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgroup',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(related_name='teachers', to='main.subject', verbose_name='Предметы'),
        ),
        migrations.DeleteModel(
            name='TeacherSubject',
        ),
    ]
