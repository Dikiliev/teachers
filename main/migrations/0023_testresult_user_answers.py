# Generated by Django 5.0.6 on 2024-07-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_question_answer_test_question_test_testresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='user_answers',
            field=models.JSONField(blank=True, null=True, verbose_name='Ответы пользователя'),
        ),
    ]
