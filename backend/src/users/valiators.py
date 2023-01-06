from django.core.exceptions import ValidationError


def validate_prohibited_name(value):
    """Проверка запрещенных имен."""
    if value.lower() == "me":
        raise ValidationError('Запрещено использовать "me"!')
