# Generated by Django 3.2.9 on 2021-11-09 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginpage', '0003_auto_20211109_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/static/no_avatar.png', upload_to='static/avatars/', verbose_name='avatar'),
        ),
    ]
