from django.contrib.auth import get_user_model # временно (импорт стандартной мадели юзер)
from django.db import models
from django.db.models import Q

User = get_user_model()  # Временно пока не создана кастомная модель User


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


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    score = models.PositiveIntegerField() # тут еще валидация нужна будет для оценок от 1 до 10
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
  
    # проверка что поле 1 <= score <= 10 ????   
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=(models.Q(score__gte=1) & models.Q(score__lte=10)),
    #             name='Оценка должна быть в деапазоне от 1 до 10'),    
    #     ]

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
        ordering = ["pub_date"]
    
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
        null=True,
        verbose_name='Раздел категории',
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=True,
        verbose_name='Раздел жанра',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
    )
