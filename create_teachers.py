import os
import django
from faker import Faker
import random
from datetime import datetime, date, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import User, Teacher, Subject, StudentGroup, Schedule

fake = Faker('ru_RU')

subjects = list(Subject.objects.all())
skills = [
    'Преподаватель математики',
    'Кандидат физико-математических наук',
    'Автор видеокурсов подготовки к ОГЭ и ЕГЭ.'
]

def create_random_student_group(user):
    group_name = fake.unique.word().capitalize() + " Group"
    price = round(random.uniform(1, 15)) * 500

    group, created = StudentGroup.objects.get_or_create(name=group_name, teacher_id=user.profile.user.id, defaults={'price': price})
    return group

def create_random_user():
    while True:
        username = fake.unique.user_name()
        email = fake.unique.email()

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password='password123')
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.phone_number = fake.phone_number()
            user.role = 2  # Роль "Преподаватель"
            user.save()
            return user

def round_time_to_nearest_half_hour(input_time):
    hour = input_time.hour
    minute = input_time.minute
    if minute < 15:
        minute = 0
    elif minute < 45:
        minute = 30
    else:
        minute = 0
        hour += 1
    return time(hour, minute)

def create_random_schedule(teacher, student_group, subject):
    days_of_week = [1, 2, 3, 4, 5, 6, 7]
    start_time = round_time_to_nearest_half_hour(fake.time_object())
    end_time = (datetime.combine(date.today(), start_time) + timedelta(hours=2)).time()
    day_of_week = random.choice(days_of_week)
    schedule, created = Schedule.objects.get_or_create(
        teacher=teacher,
        student_group=student_group,
        subject=subject,
        defaults={
            'day_of_week': day_of_week,
            'start_time': start_time,
            'end_time': end_time
        }
    )
    return schedule


def generate_achievements(subjects):
    achievements = [
        "Публикация научной статьи",
        'Кандидат наук',
        'Автор видеокурсов подготовки к ОГЭ и ЕГЭ.'
    ]

    achievements += [f'Преподователь {subject.name.lower()}' for subject in subjects]

    result = random.sample(achievements, k=random.randint(2, 3))
    return '\n'.join(result)


def create_random_teacher():
    user = create_random_user()
    teacher, created = Teacher.objects.get_or_create(user=user)

    assigned_subjects = random.sample(subjects, k=random.randint(1, len(subjects) // 3))
    assigned_groups = [create_random_student_group(user) for _ in range(random.randint(1, 4))]
    teacher.subjects.set(assigned_subjects)

    teacher.skills = generate_achievements(assigned_subjects)

    teacher.save()

    for group in assigned_groups:
        for subject in assigned_subjects:
            create_random_schedule(teacher, group, subject)

    return teacher


num_teachers = 15
for _ in range(num_teachers):
    teacher = create_random_teacher()
    print(f'Создан {teacher}')

print(f'{num_teachers} преподавателей успешно созданы!')
