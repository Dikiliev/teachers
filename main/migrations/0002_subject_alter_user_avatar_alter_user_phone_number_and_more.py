# Generated by Django 5.0.6 on 2024-05-31 21:40

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название предмета')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png', upload_to='', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть в формате: '+999999999'. Допустимо до 15 цифр.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Пользователь'), (2, 'Преподаватель'), (3, 'Менеджер')], default=1, verbose_name='Роль'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teacher_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, verbose_name='Биография')),
                ('subjects', models.ManyToManyField(related_name='teachers', to='main.subject', verbose_name='Предметы')),
            ],
        ),
    ]
