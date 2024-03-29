from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

from api_yamdb.constants import MAX_SLUG_LENGTH
from core.models import (
    BaseReviewModel, BaseNameModel
)

User = get_user_model()


class Category(BaseNameModel):
    slug = models.SlugField(
        verbose_name="Slug категории", max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Genre(BaseNameModel):
    slug = models.SlugField(
        verbose_name="Slug жанра", max_length=MAX_SLUG_LENGTH
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Title(BaseNameModel):
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
        null=True,
        blank=True,
        validators=[MaxValueValidator(timezone.now().year)],
    )
    rating = models.FloatField(
        verbose_name="Рейтинг произведения",
        default=None,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание", blank=True, default=""
    )
    genre = models.ManyToManyField(
        Genre, verbose_name="Slug жанра", through="GenreTitle"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Slug категории",
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        Genre, verbose_name="Жанр", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведений"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title - self.genre


class Review(BaseReviewModel):
    title = models.ForeignKey(
        Title,
        verbose_name="ID произведения",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка произведения",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=10),
        ],
    )
    author = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [("title", "author")]
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def calc_average_score():
        return Review.objects.aggregate(models.Avg("score"))["score__avg"] or 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.rating = self.calc_average_score()
        self.title.save()


class Comment(BaseReviewModel):
    review = models.ForeignKey(
        Review,
        verbose_name="ID обзора",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.text
