from django.db import models
from django.templatetags.static import static


class CustomUser(models.Model):
    email = models.EmailField('email', max_length=100, unique=True)
    username = models.CharField('username', max_length=100, unique=True)
    password = models.CharField('password', max_length=255)
    role = models.BooleanField('is_admin', default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField('Name', max_length=30, default='Человек')
    lastname = models.CharField('Lastname', max_length=30, default='Неизвестный')
    avatar = models.ImageField('avatar', upload_to='avatars/%b%d%Y%H%M%S/', default=static('no_avatar.png'))
    genders = (('m', 'Мужчина'),
               ('f', 'Женщина'))
    gender = models.CharField('Пол', max_length=10, choices=genders, default='не указан')

    def __str__(self):
        return self.user.username
