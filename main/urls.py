from django.urls import path, register_converter
from . import views, converters

register_converter(converters.IntListConverter, 'intlist')
register_converter(converters.DateTimeConverter, 'datetime')

WORKER = 'w'
SUBJECT = 's'
GROUP = 'd'

register_converter(converters.IntListConverter, 'intlist')
register_converter(converters.DateTimeConverter, 'datetime')

urlpatterns = [
    path('', views.home, name='home'),

    path(f'select_teacher', views.select_teacher, name='select_teacher'),

    path(f'select_teacher/{WORKER}<int:teacher_id>{SUBJECT}<int:subject_id>{GROUP}<int:group_id>',
         views.select_teacher, name='select_teacher'),

    path(f'select_subject/{WORKER}<int:teacher_id>{SUBJECT}<int:subject_id>{GROUP}<int:group_id>',
         views.select_subject, name='select_subject'),

    path(f'select_group/{WORKER}<int:teacher_id>{SUBJECT}<int:subject_id>{GROUP}<int:group_id>',
         views.select_group, name='select_group'),

    path(f'get_teachers/<int:subject_id>', views.get_teachers, name='get_teachers'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
