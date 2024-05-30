import datetime
import json

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from main.models import User

DEFAULT_TITLE = 'Хехархо'

def home(request: HttpRequest):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    context = create_base_data(request)
    return render(request, 'index.html', context)


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

        if user.role == 2:
            profile = Profile(user=user)
            profile.save()
            return redirect('profile')

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    data = create_base_data(request)

    def get():

        # jinja2_engine = engines['jinja2']
        # template = jinja2_engine.get_template('registration/login.html')
        # rendered_template = template.render(data)
        # return HttpResponse(rendered_template)

        return render(request, 'registration/login.html', data)

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        data['username'] = request.POST['username']

        if user is not None:
            login(request, user)

            if user.role == 1:
                return redirect('home')

            return redirect('orders')

        data['error'] = '* Неверное имя пользователя или пароль'

        return render(request, 'registration/login.html', data)

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