from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .valiators import validate_prohibited_name

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLE_CHOICES = (
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор")
)


class User(AbstractUser):
    """Расширенная модель пользователя."""

    username = models.CharField(
        max_length=settings.MAX_LENGTH_USER_MODEL_FIELD,
        unique=True,
        verbose_name="Логин",
        help_text="Придумайте уникальный логин",
        validators=[UnicodeUsernameValidator(),
                    validate_prohibited_name]
    )
    email = models.EmailField(
        max_length=settings.MAX_LENGTH_USER_EMAIL,
        unique=True,
        verbose_name="Адрес электронной почты",
        help_text="Введите адрес электронной почты"
    )
    role = models.CharField(
        max_length=settings.MAX_LENGTH_USER_ROLE,
        verbose_name="Роль пользователя",
        help_text="Выберите роль пользователю",
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_staff

    @property
    def is_user(self):
        return self.role == USER
