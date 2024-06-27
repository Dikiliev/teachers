from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html

from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

from .admin_filters import TeacherFilter
from .forms import ScheduleForm
from .models import User, Teacher, Subject, StudentGroup, Schedule, Appointment, AppointmentStatus, Application


class UserCreationForm(forms.ModelForm):
    """Форма для создания нового пользователя. Включает все необходимые поля, плюс повторение пароля."""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'avatar', 'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Форма для обновления пользователя. Включает все поля пользователя, но заменяет поле пароля на админское поле
    отображения пароля."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'first_name', 'last_name', 'role', 'avatar', 'phone_number', 'is_active', 'is_staff'
        )


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Преподаватели'
    fields = ('bio', 'subjects', 'skills')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'phone_number')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Роль', {'fields': ('role', 'view_teacher_profile',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')}
         ),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ['view_teacher_profile']  # Make the button read-only

    def view_teacher_profile(self, obj):
        if obj.role == 2 and hasattr(obj, 'profile'):  # Assuming 2 is the value for the Teacher role
            link = reverse('admin:main_teacher_change', args=[obj.profile.pk])
            return format_html('<a class="btn btn-info form-control" href="{}">Перейти на профиль преподавателя</a>', link)
        return 'Нет профиля преподавателя'
    view_teacher_profile.short_description = 'Профиль преподавателя'
    view_teacher_profile.allow_tags = True


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


class StudentGroupInline(admin.TabularInline):
    model = StudentGroup
    extra = 1
    verbose_name = "Группа студентов"
    verbose_name_plural = "Группы студентов"


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    inlines = [StudentGroupInline, ScheduleInline]


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject')
    search_fields = ('name', 'subject__name', 'teacher__user__username', 'teacher__user__first_name', 'teacher__user__last_name')
    list_filter = ('subject', TeacherFilter)


class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = ('teacher', 'student_group', 'day_of_week', 'start_time', 'formatted_duration')
    list_filter = ('day_of_week', 'teacher', 'student_group')
    search_fields = ('teacher__user__username', 'student_group__name')

    def formatted_duration(self, obj):
        total_minutes = obj.duration.total_seconds() // 60
        hours = total_minutes // 60
        minutes = total_minutes % 60

        if minutes == 0:
            return f'{int(hours)}ч'
        return f'{int(hours)}ч {int(minutes)}мин'
    formatted_duration.short_description = 'Длительность'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_user_display', 'group', 'user_name', 'user_phone', 'created_at', 'status')
    search_fields = ('user__username', 'user_name', 'group__name')
    list_filter = ('group', 'created_at', 'status')
    fields = ('user', 'group', 'user_name', 'user_phone', 'user_comment', 'created_at', 'status')
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if obj.status == AppointmentStatus.ACCEPTED.name and obj.user is None:
            messages.error(request, "Невозможно принять запись без зарегистрированного пользователя.")
            return

        if change:
            old_status = Appointment.objects.get(pk=obj.pk).status
            if old_status != AppointmentStatus.ACCEPTED.name and obj.status == AppointmentStatus.ACCEPTED.name:
                if obj.user is not None:
                    obj.group.students.add(obj.user)
                    messages.add_message(request, messages.SUCCESS, 'Пользователь был добавлен в группу.')
            elif old_status == AppointmentStatus.ACCEPTED.name and obj.status != AppointmentStatus.ACCEPTED.name:
                if obj.user is not None:
                    obj.group.students.remove(obj.user)
                    messages.add_message(request, messages.SUCCESS, 'Пользователь был удален из группы.')

        super().save_model(request, obj, form, change)

    def get_user_display(self, obj):
        if obj.user is None:
            return 'не зарегистрирован'
        return obj.user.username
    get_user_display.short_description = 'User'


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_phone', 'subject', 'created_at', 'updated_at')
    search_fields = ('user_name', 'user_phone', 'subject__name')
    list_filter = ('subject', 'created_at', 'updated_at')
    fields = ('user', 'user_name', 'user_phone', 'subject', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.user and not obj.user_name:
            messages.error(request, "Имя пользователя обязательно, если пользователь не зарегистрирован.")
            return

        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Application, ApplicationAdmin)
