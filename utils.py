# utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_status_change_email(user_email, application, new_status):
    subject = f"Изменение статуса заявления #{application.id}"
    message = f"Здравствуйте, {application.student.username}!\n\n" \
              f"Статус вашего заявления \"{application.application_type.name}\" был изменен на \"{new_status}\".\n\n" \
              f"Дата подачи: {application.submission_date}\n" \
              f"Текущий статус: {new_status}\n\n" \
              f"С уважением,\nКоманда поддержки."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
