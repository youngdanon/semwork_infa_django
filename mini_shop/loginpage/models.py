from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)


# class CustomUser(AbstractUser):
#     genders = (('m', 'Мужчина'), ('f', 'Женщина'))
#     gender = models.CharField('Пол', max_length=10, choices=genders, default='')
#     date_of_birth = models.DateField('Дата рождения', default='2000-09-12')

class CustomUser(models.Model):
    email = models.EmailField('email', max_length=100, unique=True)
    username = models.CharField('username', max_length=100, unique=True)
    password = models.CharField('password', max_length=255)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField('Name', max_length=30)
    lastname = models.CharField('Lastname', max_length=30)
    avatar = models.ImageField('avatar', upload_to='assets/avatars/', default='assets/no_avatar.png')
    genders = (('m', 'Мужчина'),
               ('f', 'Женщина'))
    gender = models.CharField('Пол', max_length=10, choices=genders)

    def __str__(self):
        return self.user.username
