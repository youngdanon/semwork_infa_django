# Generated by Django 3.2.9 on 2021-11-09 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginpage', '0005_auto_20211109_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/static/no_avatar.png', height_field=300, upload_to='static/avatars/', verbose_name='avatar', width_field=300),
        ),
    ]
