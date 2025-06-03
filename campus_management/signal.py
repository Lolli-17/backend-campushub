from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from random import randrange
# from .models import OneTimePassword
# from django.core.mail import send_mail


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_one_time_passowrd(sender, instance=None, created=False, **kwargs):
#     if created:
#         otp = randrange(100000, 1000000)
#         OneTimePassword.objects.create(id=instance, password=otp)
#         send_mail(
#             'Beccati sto otp',
#             f'Questo è l\'otp: {otp}',
#             'from@example.com',
#             ['to@example.com'],
#             fail_silently=False,
#         )