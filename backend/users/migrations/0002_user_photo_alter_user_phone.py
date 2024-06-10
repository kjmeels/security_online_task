# Generated by Django 5.0.1 on 2024-06-10 07:00

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to='u/u/p', verbose_name='Фото пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=13, region=None, verbose_name='Телефон'),
        ),
    ]