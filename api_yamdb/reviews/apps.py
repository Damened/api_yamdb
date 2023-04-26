from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    # строка создана при создании приложения без нее возникают ошибки с авто-заполняемыми полями
    default_auto_field = 'django.db.models.BigAutoField' 
    name = 'reviews'
    verbose_name = 'Отзывы'
