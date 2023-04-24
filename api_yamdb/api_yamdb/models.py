from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Раздел категории',
    )


class Genre(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        verbose_name='Раздел жанра',
    )


class Title(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL)
