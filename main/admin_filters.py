from django.contrib.admin import SimpleListFilter

class TeacherFilter(SimpleListFilter):
    title = 'Преподаватель'
    parameter_name = 'teacher'

    def lookups(self, request, model_admin):
        teachers = set([c.teacher for c in model_admin.model.objects.all()])
        return [(t.user.id, f"{t.user.first_name} {t.user.last_name} ({t.user.username})") for t in teachers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(teacher__user__id=self.value())
        return queryset
