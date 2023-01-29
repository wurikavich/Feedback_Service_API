from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from src.titles.validators import NameValidator, SlugValidator


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        unique=True,
        verbose_name="Название",
        help_text="Введите название категории"
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True,
        verbose_name="Slug",
        help_text="Введите slug для категории",
        validators=(SlugValidator(),)
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        unique=True,
        verbose_name="Название",
        help_text="Введите название жанра",
        validators=(NameValidator(),)
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True,
        verbose_name="Slug",
        help_text="Введите slug для жанра",
        validators=(SlugValidator(),)
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name="Название",
        help_text="Введите название произведения"
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
        help_text="Добавьте год выпуска произведения",
        validators=[
            MaxValueValidator(
                limit_value=date.today().year,
                message="Нельзя добавлять не выпущенные произведения!")
        ]
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
        help_text="Добавьте описание произведения"
    )
    genre = models.ManyToManyField(
        Genre,
        symmetrical=False,
        related_name='+',
        verbose_name="Жанры",
        help_text="Выберите жанры"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='+',
        verbose_name="Категория",
        help_text="Выберите категорию"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition of an title if present',
                fields=['name', 'year'])
        ]

    def __str__(self):
        return self.name
