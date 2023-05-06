from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from users.models import User


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.PositiveIntegerField() # тут еще валидация нужна будет для оценок от 1 до 10
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    def clean(self):
       if self.score > 10: # проверяет чтобы score было от 1 до 10, но работает только для админки
            raise ValidationError('Оценка должна быть в деапазоне от 1 до 10')
  
    class Meta:
        ordering = ["-pub_date"]

        '''Ограничения на внесение изменений в БД'''    
        constraints = [
            models.CheckConstraint(
                check=(models.Q(score__gte=1)&models.Q(score__lte=10)),
                name='Оценка должна быть в деапазоне от 1 до 10'),
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='К произведению нельзя оставить более одного отзыва'),       
        ]

    def __str__(self):
        return f'{self.text} отзыв к произведению {self.title}'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ["-pub_date"]
    
    def __str__(self):
        return f'{self.text} комментарий к отзыву {self.review}'



class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Раздел категории',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Раздел жанра',
    )

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} {self.slug}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
