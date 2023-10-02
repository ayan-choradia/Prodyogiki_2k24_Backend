# tasks.py

from celery import shared_task
from .models import CustomUser
from django.core.mail import send_mail, EmailMessage, get_connection
from core import settings


# @shared_task
# def test_celery_connection():
#     print("Celery connection successful!")


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"


# @shared_task(bind=True)
# def send_mail_func(self):
#     users = CustomUser.objects.all()
#     for user in users:
#         if user.email == "aggarwalmehul26@gmail.com" or user.email == "21BMA003@nith.ac.in":
#             print(user.username)
#             mail_subject = "Hi! Celery Testing"
#             message = f"Hi {user.username}. This is the celery test mail"
#             to_email = user.email
#             send_mail(
#                 subject=mail_subject,
#                 message=message,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[to_email],
#                 fail_silently=True
#             )
#     return "Done"

@shared_task(bind=True)
def send_mail_func(self):
    users = CustomUser.objects.filter(
        email__in=["aggarwalmehul26@gmail.com", "21BMA003@nith.ac.in"]
    )
    if users:
        mail_subject = "Hi! Celery Testing"
        message = "Hi {username}. This is the celery test mail"
        recipients = [(user.username, user.email) for user in users]

        email_messages = [
            EmailMessage(
                subject=mail_subject,
                body=message.format(username=username),
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            for username, email in recipients
        ]

        connection = get_connection()
        connection.send_messages(email_messages)

        return f"Sent {len(email_messages)} emails"

    return "No matching users found"
