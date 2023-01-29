from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.titles.models import Title
from src.users.models import User


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Прокомментированное произведение"
    )
    text = models.TextField(
        verbose_name="Отзыв о произведении",
        help_text="Напишите отзыв произведению"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка произведению",
        help_text="Дайте оценку произведению от 1 до 10",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                name='exclude the addition of an review if present',
                fields=['title', 'author'])
        ]

    def __str__(self):
        return (f'"{self.author}" добавил отзыв на "{self.title}"'
                f' с оценкой "{self.score}".')


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Прокомментированный отзыв"
    )
    text = models.TextField(
        verbose_name="Комментарий пользователя",
        help_text="Напишите комментарий"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'

    def __str__(self):
        return f'"{self.author}" прокомментировал отзыв c id {self.review.id}'
