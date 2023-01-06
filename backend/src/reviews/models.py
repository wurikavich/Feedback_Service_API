from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import SlugValidator
from ..users.models import User


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
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        unique=True,
        verbose_name="Название",
        help_text="Введите название жанра"
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True,
        verbose_name="Slug",
        help_text="Введите slug для жанра",
        validators=(SlugValidator(),)
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

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
                message="Нельзя добавлять не выпущенные произведения!")]
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
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        constraints = [
            models.UniqueConstraint(
                name="exclude the addition of an title if present",
                fields=["name", "year"])
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Автор"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
        help_text="Выберите произведение"
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Напишите свой отзыв"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка зрителя",
        help_text="Дайте оценку произведению от 1 до 10",
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                name="exclude the addition of an review if present",
                fields=["title", "author"])
        ]

    def __str__(self):
        return (f'"{self.author}" добавил отзыв на "{self.title}"'
                f' с оценкой "{self.score}".')


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name="Автор"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
        help_text="Выберите отзыв"
    )
    text = models.TextField(
        verbose_name="Комментарий",
        help_text="Оставьте свой комментарий к отзыву"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзывам"

    def __str__(self):
        return f'"{self.author}" прокомментировал отзыв c id {self.review.id}'
