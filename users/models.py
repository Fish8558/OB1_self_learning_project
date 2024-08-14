from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    class UsersRolesChoices(models.TextChoices):
        STUDENT = 'student', _('Студент')
        PROFESSOR = 'professor', _('Преподаватель')
        ADMIN = 'admin', _('Администратор')

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    user_name = models.CharField(max_length=50, unique=True, verbose_name='Никнейм')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Телефон')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='Город')
    role = models.CharField(max_length=10, choices=UsersRolesChoices,
                            default=UsersRolesChoices.STUDENT, verbose_name='Роль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
