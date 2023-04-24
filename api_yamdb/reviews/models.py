from django.contrib.auth import get_user_model # временно (импорт стандартной мадели юзер)
from django.db import models

User = get_user_model() # Временно пока не создана кастомная модель User


class Title(models.Model): # Временно пока нет модели для произведений
    pass

class Reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    def __str__(self):
        return f'{self.text} отзыв к произведению {self.reviews}'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    reviews = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    def __str__(self):
        return f'{self.text} комментарий к отзыву {self.reviews}'