from django import forms
from .models import Schedule, StudentGroup, Teacher

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'teacher' in self.data:
            try:
                teacher_id = int(self.data.get('teacher'))
                self.fields['student_group'].queryset = StudentGroup.objects.filter(teacher_id=teacher_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['student_group'].queryset = self.instance.teacher.groups.all()
        else:
            self.fields['student_group'].queryset = StudentGroup.objects.none()
