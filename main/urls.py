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

    path(f'get_teachers/<int:subject_id>', views.get_teachers, name='get_teachers'),
    path(f'get_groups/<int:teacher_id>', views.get_groups, name='get_groups'),
    path(f'get_group/<int:teacher_id>/<int:group_id>', views.get_group, name='get_group'),

    path(f'confirm_appointment/<int:group_id>', views.confirm_appointment, name='confirm_appointment'),
    path(f'appointment_completed', views.appointment_completed, name='appointment_completed'),

    path('profile/', views.profile, name='profile'),
    path('my_groups/', views.my_groups, name='my_groups'),
    path('manage_groups/', views.manage_groups, name='manage_groups'),
    path('manage_group/<int:group_id>', views.manage_group, name='manage_group'),
    path('group_students/<int:group_id>', views.group_students, name='group_students'),

    path('save_group/<int:group_id>', views.save_group, name='save_group'),
    path('delete_group/<int:group_id>', views.delete_group, name='delete_group'),


    path('send_results/', views.send_results, name='send_results'),
    path('test/<int:subject_id>', views.test, name='test'),
    path('test_result/<int:result_id>/', views.test_result_view, name='test_result_view'),


    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),


    # ----- MANAGER ----- #
    path('manager_home/', views.manager_home, name='manager_home'),
    path('manager_appointments/', views.manager_appointments, name='manager_appointments'),

    path('set_appointment_status/', views.set_appointment_status, name='set_appointment_status'),
    # path('manage_group', views.manage_group, name='manage_group'),
]
