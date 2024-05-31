from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):

    ROLE_ENUM = (
        (1, 'Пользователь'),
        (2, 'Преподаватель'),
        (3, 'Менеджер'),
    )

    DEFAULT_AVATAR_URL = 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'

    role = models.IntegerField(
        choices=ROLE_ENUM,
        default=1,
        verbose_name='Роль'
    )

    avatar = models.ImageField(
        blank=True,
        default=DEFAULT_AVATAR_URL,
        verbose_name='Аватарка'
    )

    phone_number = models.CharField(
        max_length=25,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'. Допустимо до 15 цифр."
            )
        ],
        verbose_name='Номер телефона'
    )

    def __str__(self):
        return f'{self.username} ({dict(self.ROLE_ENUM).get(self.role, "Неизвестная роль")})'

    @classmethod
    def user_exists(cls, username):
        return cls.objects.filter(username=username).exists()


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teacher_profile'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', verbose_name='Предметы')

    def __str__(self):
        return f'{self.user.username} - Преподаватель'
