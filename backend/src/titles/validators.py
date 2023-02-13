from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator(RegexValidator):
    """Проверка Названия на валидность."""

    regex = r"^[а-яА-ЯёЁa-zA-Z0-9]+$"
    message = "Недопустимый формат Названия!"
    flag = 0


@deconstructible
class SlugValidator(RegexValidator):
    """Проверка Slug на валидность."""

    regex = r"^[-a-zA-Z0-9_]+$"
    message = "Недопустимый формат Slug-a!"
    flags = 0
