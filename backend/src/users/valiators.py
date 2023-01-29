from django.conf import settings
from django.core.exceptions import ValidationError


def validate_prohibited_name(value):
    """Проверка запрещенных имен."""
    if value.lower() in settings.FORBIDDEN_NAMES:
        raise ValidationError(f"Использовать '{value}' запрещено!")
