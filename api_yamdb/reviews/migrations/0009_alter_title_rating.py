# Generated by Django 3.2 on 2023-10-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_alter_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.FloatField(verbose_name='Рейтинг произведения'),
        ),
    ]
