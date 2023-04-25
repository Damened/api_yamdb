from django.db import models


class Category(models.Model):
    name = models.CharField( #исправил на name
        max_length=256, #исправил на 256
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50, #добавил длину
        unique=True,
        null=False,
        verbose_name='Раздел категории',
    )


class Genre(models.Model):
    name = models.CharField( #исправил на name
        max_length=256, #исправил
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50, #добавил
        unique=True,
        null=False,
        verbose_name='Раздел жанра',
    )


class Title(models.Model):
    name = models.CharField( #изменил на name
        max_length=256, #добавил
        verbose_name='Название произведения',
    )
    year = models.IntegerField( #добавил
        verbose_name='Год выпуска',
    )
    description = models.CharField( #добавил
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles', #добавил
        verbose_name='Категория произведения',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='titles', #добавил
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
    )
