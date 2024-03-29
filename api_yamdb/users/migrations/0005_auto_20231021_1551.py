# Generated by Django 3.2 on 2023-10-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Является администратором'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_moderator',
            field=models.BooleanField(default=False, verbose_name='Является модератором'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=150, verbose_name='Роль'),
        ),
    ]
