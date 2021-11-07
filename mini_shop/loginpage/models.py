from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)

class CustomUser(AbstractUser):
    genders = (('m', 'Мужчина'), ('f', 'Женщина'))
    gender = models.CharField('Пол', max_length=10, choices=genders, default='')
    date_of_birth = models.DateField('Дата рождения', default='2000-09-12')


