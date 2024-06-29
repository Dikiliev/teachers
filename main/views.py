import datetime
import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from main.models import User, Subject, Teacher, StudentGroup, Appointment, UserRole, Schedule, Application

DEFAULT_TITLE = 'Хехархо'


def home(request: HttpRequest):
    context = create_base_data(request)
    context['subjects'] = Subject.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        subject_id = request.POST.get('category')

        if subject_id == "0":
            context['error'] = 'Пожалуйста, выберите предмет.'
        else:
            subject = Subject.objects.get(id=subject_id)

            Application.objects.create(
                user_name=first_name,
                user_phone=phone,
                subject=subject
            )

            return redirect('appointment_completed')

    return render(request, 'index.html', context)


def select_teacher(request: HttpRequest):
    context = create_base_data(request)
    context['subjects'] = Subject.objects.all()

    return render(request, 'teachers.html', context)


def create_context_for_appointment(context: dict, group: StudentGroup):
    teacher = group.teacher
    group_info = {
        'id': group.id,
        'name': group.name,
        # 'price': group.price,
        'subject': group.subject,
        'schedules': [{
            'day_of_week': schedule.get_day_of_week_display(),
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
        } for schedule in group.schedules.all()],
    }

    context['teacher'] = teacher
    context['teacher'] = {
        'id': teacher.user.id,
        'name': teacher.user.get_full_name(),
        'avatar_url': teacher.user.get_avatar_url(),
        'skills': teacher.skills.split('\n')
    }
    context['group'] = group_info
    return context


def confirm_appointment(request: HttpRequest, group_id: int):
    context = create_base_data(request)

    if request.method == 'POST':
        appointment = Appointment()

        if request.user.is_authenticated:
            appointment.user = request.user
        appointment.group_id = group_id

        appointment.user_name = request.POST.get('fullname', '')
        appointment.user_phone = request.POST.get('phone', '')
        appointment.user_comment = request.POST.get('comment', '')

        appointment.save()

        return redirect('appointment_completed')

    group = StudentGroup.objects.get(id=group_id)
    user = request.user if request.user.is_authenticated else None

    context = create_context_for_appointment(context, group)

    return render(request, 'appointment.html', context)


def appointment_completed(request: HttpRequest):
    context = create_base_data(request)

    # group = StudentGroup.objects.get(id=group_id)
    # context = create_context_for_appointment(context, group)

    return render(request, 'appointment_completed.html', context)


def get_teachers(request: HttpRequest, subject_id):
    data = dict()

    try:
        if subject_id:
            subject = Subject.objects.get(pk=subject_id)
            teachers = Teacher.objects.filter(subjects=subject)
        else:
            teachers = Teacher.objects.all()

        teacher_list = []
        for teacher in teachers:
            teacher_info = {
                'id': teacher.user.id,
                'name': teacher.user.get_full_name(),
                'avatar': teacher.user.get_avatar_url(),
                'groups': [group.name for group in teacher.groups.all()],
                'skills': teacher.skills.split('\n') if teacher.skills else [],
            }
            teacher_list.append(teacher_info)

        data['message'] = 'success'
        data['teachers'] = teacher_list

    except Subject.DoesNotExist:
        data['message'] = 'Subject not found'

    return JsonResponse(data)


def get_groups(request: HttpRequest, teacher_id: int):
    data = dict()

    try:
        teacher = Teacher.objects.get(pk=teacher_id)

        groups = StudentGroup.objects.filter(teacher=teacher)
        group_list = []
        for group in groups:
            group_info = {
                'id': group.id,
                'name': group.name,
                'subject': {'id': group.subject.id, 'name': group.subject.name},
                # 'price': group.price,
                'schedules': [{
                    'day_of_week': schedule.day_of_week,
                    'day_of_week_display': schedule.get_day_of_week_display(),
                    'start_time': schedule.start_time.strftime('%H:%M'),
                    'end_time': schedule.end_time.strftime('%H:%M'),
                    'duration_minutes': schedule.duration.total_seconds() // 60,
                } for schedule in group.schedules.all()],
            }
            group_list.append(group_info)

        data['groups'] = group_list

        available_subjects = teacher.subjects.all()
        data['available_subjects'] = [{'id': subject.id, 'name': subject.name} for subject in available_subjects]
        data['days_of_week'] = Schedule.DAYS_OF_WEEK

        data['message'] = 'success'

    except Subject.DoesNotExist:
        data['message'] = 'Subject not found'

    print(data)
    return JsonResponse(data)


def get_group(request: HttpRequest, teacher_id, group_id: int):
    data = dict()

    teacher = Teacher.objects.get(pk=teacher_id)
    available_subjects = teacher.subjects.all()
    data['available_subjects'] = [{'id': subject.id, 'name': subject.name} for subject in available_subjects]
    data['days_of_week'] = Schedule.DAYS_OF_WEEK

    if group_id == 0:
        data['group'] = {
            'name': '',
            'subject': {'id': 0, 'name': ''},
            'schedules': [{}]
        }

        return JsonResponse(data)

    try:
        group = StudentGroup.objects.get(id=group_id)

        group_info = {
            'id': group.id,
            'name': group.name,
            'subject': {'id': group.subject.id, 'name': group.subject.name},
            # 'price': group.price,
            'schedules': [{
                'day_of_week': schedule.day_of_week,
                'start_time': schedule.start_time.strftime('%H:%M'),
                'end_time': schedule.end_time.strftime('%H:%M'),
                'duration_minutes': schedule.duration.total_seconds() // 60,
            } for schedule in group.schedules.all()],
        }

        data['group'] = group_info

        data['message'] = 'success'

    except Subject.DoesNotExist:
        data['message'] = 'Subject not found'

    print(data)
    return JsonResponse(data)


@login_required
def profile(request: HttpRequest):
    context = create_base_data(request)
    user = request.user
    context['username'] = user.username

    if user.role == 2:
        context['subjects'] = Subject.objects.all()
        context['selected_subjects'] = user.profile.subjects.all()

    def get():
        return render(request, 'profile.html', context)

    def post():
        post_data = request.POST
        uploaded_image = request.FILES.get('image_file', None)

        if uploaded_image:
            user.avatar = uploaded_image

        subjects = Subject.objects.filter(id__in=post_data.getlist('subjects', []))
        user.profile.subjects.set(subjects)

        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.skills = request.POST.get('about', '')

        user.phone_number = post_data.get('phone', '')

        user.profile.save()
        user.save()

        context['message'] = 'Сохранено!'

        messages.success(request, 'Profile updated successfully')
        return render(request, 'profile.html', context)

    if request.method == 'POST':
        return post()

    return get()


@login_required
def my_groups(request: HttpRequest):
    context = create_base_data(request)

    def get():
        user = request.user
        groups = user.student_groups.all()
        groups = groups.annotate(students_count=Count('students'))

        print(groups)

        context['groups'] = groups
        return render(request, 'my_groups.html', context)

    def post():
        return render(request, 'my_groups.html', context)

    if request.method == 'POST':
        return post()

    return get()


@login_required
def manage_groups(request: HttpRequest):
    if not hasattr(request.user, 'profile'):
        return redirect('home')

    context = create_base_data(request)

    user = request.user
    groups = StudentGroup.objects.filter(teacher=user.profile)
    groups = groups.annotate(students_count=Count('students'))

    context['groups'] = groups

    def get():
        return render(request, 'manage_groups.html', context)

    def post():
        return render(request, 'manage_groups.html', context)

    if request.method == 'POST':
        return post()

    return get()


@login_required
def manage_group(request: HttpRequest, group_id):
    if not hasattr(request.user, 'profile'):
        return redirect('home')

    context = create_base_data(request)
    context['subjects'] = Subject.objects.all()

    user = request.user

    # group = StudentGroup.objects.get(pk=group_id)
    context['group_id'] = group_id
    context['teacher'] = user.profile

    return render(request, 'manage_group.html', context)


@csrf_exempt
def save_group(request: HttpRequest, group_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)

        group = StudentGroup.objects.get(pk=group_id) if group_id != 0 else StudentGroup(teacher=request.user.profile)

        group.name = data['name']
        group.subject_id = data['subject']['id']
        group.save()

        # Обновление существующих расписаний или создание новых
        existing_schedules = {s.id: s for s in Schedule.objects.filter(student_group=group)}

        for schedule_data in data.get('schedules', []):
            schedule_id = schedule_data.get('id')
            if schedule_id and schedule_id in existing_schedules:
                # Обновление существующего расписания
                schedule = existing_schedules[schedule_id]
                schedule.day_of_week = schedule_data['day_of_week']
                schedule.start_time = schedule_data['start_time']
                schedule.duration = datetime.timedelta(minutes=int(schedule_data['duration_minutes']))
                schedule.save()
                del existing_schedules[schedule_id]
            else:
                # Создание нового расписания
                Schedule.objects.create(
                    teacher=group.teacher,
                    student_group=group,
                    day_of_week=schedule_data['day_of_week'],
                    start_time=schedule_data['start_time'],
                    duration=datetime.timedelta(minutes=int(schedule_data['duration_minutes']))
                )

        # Удаление любых расписаний, не включенных в обновление
        for schedule in existing_schedules.values():
            schedule.delete()

        return JsonResponse({'message': 'Данные успешно сохранены.'})

    except StudentGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def delete_group(request: HttpRequest, group_id):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        group = StudentGroup.objects.get(pk=group_id)
        group.delete()

        return JsonResponse({'ok': True, 'message': 'Группа успешно удалена'})

    except StudentGroup.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Group not found'}, status=404)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@login_required
def group_students(request, group_id):
    if not hasattr(request.user, 'profile'):
        return redirect('home')

    context = create_base_data(request)

    group = StudentGroup.objects.get(pk=group_id)
    context['group'] = group
    context['students'] = group.students.all()

    def get():
        return render(request, 'group_students.html', context)

    return get()

def register(request: HttpRequest):
    context = create_base_data(request)
    context['username'] = context['first_name'] = context['last_name'] = context['phone'] = ''

    def get():
        print(context)
        return render(request, 'registration/register.html', context)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.first_name = post_data.get('first_name', '')
        user.last_name = post_data.get('last_name', '')
        user.phone_number = post_data.get('phone', '')
        user.address = post_data.get('address', '')
        user.role = 1

        password = post_data.get('password', '')

        context['username'] = user.username
        context['email'] = user.email
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['phone'] = user.phone_number

        def check_validate():
            if len(user.username) < 3:
                context['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exists():
                context['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                context['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', context)

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    context = create_base_data(request)

    def get():

        # jinja2_engine = engines['jinja2']
        # template = jinja2_engine.get_template('registration/login.html')
        # rendered_template = template.render(context)
        # return HttpResponse(rendered_template)

        return render(request, 'registration/login.html', context)

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        context['username'] = request.POST['username']

        if user is not None:
            login(request, user)

            if user.role == 1:
                return redirect('home')

            return redirect('home')

        context['error'] = '* Неверное имя пользователя или пароль'

        return render(request, 'registration/login.html', context)

    if request.method == 'POST':
        return post()
    return get()


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


def create_base_data(request: HttpRequest, title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'user': request.user,
        'title': title,
    }
