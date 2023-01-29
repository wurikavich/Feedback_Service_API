from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class SlugValidator(validators.RegexValidator):
    """Проверка slug на валидность."""
    regex = r"^[-a-zA-Z0-9_]+$"
    message = "Недопустимый формат Slug-a!"
    flags = 0
