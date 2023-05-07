import jwt
from django.db import models
from django.contrib.auth.models import AbstractUser

from .userroles import UserRoles


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    confirmation_code = models.CharField(
        max_length=254,
        verbose_name='Код подтверждения',
        blank=True,
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
    
  