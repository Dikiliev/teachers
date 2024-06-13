from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from enum import Enum


class UserRole(Enum):
    USER = 1, 'Пользователь'
    TEACHER = 2, 'Преподаватель'
    MANAGER = 3, 'Менеджер'


class DayOfWeek(Enum):
    MONDAY = 1, 'Понедельник'
    TUESDAY = 2, 'Вторник'
    WEDNESDAY = 3, 'Среда'
    THURSDAY = 4, 'Четверг'
    FRIDAY = 5, 'Пятница'
    SATURDAY = 6, 'Суббота'
    SUNDAY = 7, 'Воскресенье'


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Номер телефона должен быть в формате: '+999999999'. Допустимо до 15 цифр."
)


class User(AbstractUser):
    ROLE_ENUM = [(role.value[0], role.value[1]) for role in UserRole]

    DEFAULT_AVATAR_URL = 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'

    role = models.IntegerField(
        choices=ROLE_ENUM,
        default=UserRole.USER.value[0],
        verbose_name='Роль'
    )

    avatar = models.ImageField(
        blank=True,
        verbose_name='Аватарка'
    )

    phone_number = models.CharField(
        max_length=25,
        blank=True,
        validators=[phone_validator],
        verbose_name='Номер телефона'
    )

    def __str__(self):
        return f'{self.username} ({dict(self.ROLE_ENUM).get(self.role, "Неизвестная роль")})'

    @classmethod
    def user_exists(cls, username):
        return cls.objects.filter(username=username).exists()

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return self.DEFAULT_AVATAR_URL

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название предмета')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        verbose_name='Пользователь'
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', verbose_name='Предметы')
    skills = models.TextField(blank=True, verbose_name='Навыки')

    def __str__(self):
        return f'{self.user.username} - Преподаватель'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class StudentGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_groups', verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups', verbose_name='Преподаватель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'


class Schedule(models.Model):
    DAYS_OF_WEEK = [(day.value[0], day.value[1]) for day in DayOfWeek]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules', verbose_name='Преподаватель')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='schedules', verbose_name='Группа студентов')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    def __str__(self):
        return f'{self.teacher.user.username} - {self.student_group.name} - {self.get_day_of_week_display()}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', blank=True, null=True, verbose_name='Клиент')
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='appointments', verbose_name='Группа')

    user_name = models.CharField(max_length=150, verbose_name='Имя')
    user_phone = models.CharField(max_length=25, blank=True, validators=[phone_validator], verbose_name='Номер телефона')
    user_comment = models.TextField(blank=True, default='', verbose_name='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Запись {self.user_name} в {self.group.name}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
