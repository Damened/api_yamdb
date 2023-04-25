from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    Biography = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
