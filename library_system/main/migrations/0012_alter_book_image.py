# Generated by Django 5.0.6 on 2024-06-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='main/static/main/img', verbose_name='Фото для обложки'),
        ),
    ]
