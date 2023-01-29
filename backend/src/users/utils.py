from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response


def send_confirmation_code(request, user, email):
    """Отправка пользователю письма с кодом подтверждения."""
    code = default_token_generator.make_token(user)
    send_mail(
        subject='Feedback Service - confirmation code.',
        message=f'Добро пожаловать! Ваш код подтверждения: "{code}".',
        from_email=settings.SERVICE_EMAIL,
        recipient_list=(email,),
        fail_silently=False
    )
    return Response(request.data, status=status.HTTP_200_OK)
