from django.db import models
from django.contrib.auth.models import AbstractUser

from .userroles import UserRoles

class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    bio = models.TextField( # исправил название поля "Biography" на "bio" как в ТЗ 
        max_length=1000,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRoles.USER
