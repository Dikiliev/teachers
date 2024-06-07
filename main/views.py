import datetime
import json

from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from main.models import User, Subject, Teacher, StudentGroup

DEFAULT_TITLE = 'Хехархо'


def home(request: HttpRequest):
    context = create_base_data(request)
    return render(request, 'index.html', context)


def select_teacher(request: HttpRequest, teacher_id: int = 0, subject_id: int = 0, group_id: int = 0):
    context = create_base_data(request)
    context['teacher_id'] = teacher_id
    context['subject_id'] = subject_id
    context['group_id'] = group_id

    teachers_query = User.objects.filter(role=2)

    if subject_id != 0:
        teachers_query = teachers_query.filter(
            profile__subjects__id__in=teacher_id
        ).annotate(
            subjects_count=Count('profile__subjects', distinct=True)
        ).all()
    else:
        teachers_query = teachers_query.annotate(
            subjects_count=Count('profile__subjects')
        ).filter(
            subjects_count__gt=0
        )

    context['workers'] = teachers_query
    context['subjects'] = Subject.objects.all()

    return render(request, 'lesson_registration/teachers.html', context)


def select_subject(request: HttpRequest, teacher_id: int = 0, subject_id: int = 0, group_id: int = 0):
    context = create_base_data(request)
    context['teacher_id'] = teacher_id
    context['subject_id'] = subject_id
    context['group_id'] = group_id

    worker = User.objects.filter(id=teacher_id).first()

    if worker and worker.profile:
        context['subjects'] = worker.profile.subjects.all()
    else:
        context['subjects'] = Subject.objects.all()

    return render(request, 'lesson_registration/subject.html', context)


def select_group(request: HttpRequest, teacher_id: int, subject_id: int, group_id: int):
    context = create_base_data(request)
    context['teacher_id'] = teacher_id
    context['subject_id'] = subject_id
    context['group_id'] = group_id

    return render(request, 'lesson_registration/group.html', context)


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


def get_groups(request: HttpRequest, teacher_id, subject_id):
    data = dict()


    try:
        subject = Subject.objects.get(pk=subject_id)
        teacher_user = User.objects.filter(pk=teacher_id)

        groups = StudentGroup.objects.filter(teacher__in=teacher_user)
        group_list = []
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

            return redirect('orders')

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