from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Teacher


@receiver(post_save, sender=User)
def create_or_update_teacher_profile(sender, instance, created, **kwargs):
    if instance.role == 2:
        Teacher.objects.get_or_create(user=instance)
    elif hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.delete()
