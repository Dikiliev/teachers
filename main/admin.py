from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .admin_filters import TeacherFilter
from .models import User, Teacher, Subject, StudentGroup, Schedule, Appointment


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
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'role', 'avatar', 'phone_number', 'is_active', 'is_staff')


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
        ('Роль', {'fields': ('role',)}),
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
    list_display = ('name', 'teacher', 'price', 'subject')
    search_fields = ('name', 'subject__name', 'teacher__user__username', 'teacher__user__first_name', 'teacher__user__last_name')
    list_filter = ('subject', TeacherFilter)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student_group', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'teacher', 'student_group')
    search_fields = ('teacher__user__username', 'student_group__name')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'user_name', 'user_phone', 'created_at')
    search_fields = ('user__username', 'user_name', 'group__name')
    list_filter = ('group', 'created_at')


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Appointment, AppointmentAdmin)
