from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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
        verbose_name='Номер телефона'
    )

    def __str__(self):
        return f'{self.get_full_name()} ({self.username}) ({dict(self.ROLE_ENUM).get(self.role, "Неизвестная роль")})'

    @classmethod
    def exists(cls):
        return cls.objects.filter(username=cls.username).exists()

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
        return f'{self.user.get_full_name()} ({self.user.username})'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class StudentGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_groups', verbose_name='Предмет')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups', verbose_name='Преподаватель')

    students = models.ManyToManyField(User, related_name='student_groups', verbose_name='Студенты', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.teacher} - {self.name}'

    class Meta:
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'


class Schedule(models.Model):
    DAYS_OF_WEEK = [(day.value[0], day.value[1]) for day in DayOfWeek]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules', verbose_name='Преподаватель')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='schedules', verbose_name='Группа студентов')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    duration = models.DurationField(verbose_name='Длительность', default=timezone.timedelta(hours=2))

    @property
    def end_time(self):
        start_datetime = timezone.datetime.combine(timezone.now().date(), self.start_time)
        end_datetime = start_datetime + self.duration
        return end_datetime.time()

    def __str__(self):
        return f'{self.teacher.user.username} - {self.student_group.name} - {self.get_day_of_week_display()}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class AppointmentStatus(Enum):
    CREATED = 'Создано'
    ACCEPTED = 'Принято'
    REJECTED = 'Отклонено'

class Appointment(models.Model):
    STATUS_CHOICES = [(status.name, status.value) for status in AppointmentStatus]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', blank=True, null=True, verbose_name='Ученик')
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='appointments', verbose_name='Группа')

    user_name = models.CharField(max_length=150, verbose_name='Имя')
    user_phone = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')
    user_comment = models.TextField(blank=True, default='', verbose_name='Комментарий')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AppointmentStatus.CREATED.name, verbose_name='Статус')

    def __str__(self):
        return f'Запись {self.user_name} в {self.group.name}'

    def clean(self):
        if self.status == AppointmentStatus.ACCEPTED.name and self.user is None:
            raise ValidationError("Невозможно принять запись без зарегистрированного пользователя.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications', verbose_name='Пользователь')

    user_name = models.CharField(max_length=150, verbose_name='Имя')
    user_phone = models.CharField(max_length=25, verbose_name='Номер телефона')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='applications', verbose_name='Предмет')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Заявка {self.user_name} на {self.subject.name}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название теста')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests', verbose_name='Предмет')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    def clean(self):
        if Test.objects.filter(name=self.name, subject=self.subject).exclude(pk=self.pk).exists():
            raise ValidationError(f"Тест с именем '{self.name}' уже существует для этого предмета.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        unique_together = ('name', 'subject')


class Question(models.Model):
    text = models.TextField(verbose_name='Текст вопроса')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')

    def __str__(self):
        return f'Вопрос {self.pk}: {self.text[:50]}...'

    def clean(self):
        # Example validation: Ensure a question text is not too short
        if len(self.text) < 10:
            raise ValidationError("Текст вопроса должен содержать как минимум 10 символов.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f'Ответ {self.pk}: {self.text[:50]}...'

    def clean(self):
        # Example validation: Ensure at least one correct answer exists per question
        if self.is_correct:
            if Answer.objects.filter(question=self.question, is_correct=True).exclude(pk=self.pk).exists():
                raise ValidationError("Каждый вопрос может иметь только один правильный ответ.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results', verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_results', verbose_name='Тест')
    score = models.IntegerField(verbose_name='Баллы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.test.name} - {self.score} баллов'

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'