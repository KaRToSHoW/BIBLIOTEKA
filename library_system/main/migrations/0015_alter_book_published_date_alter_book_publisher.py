# Generated by Django 5.0.6 on 2024-06-08 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(verbose_name='Дата издания книги'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Издатель'),
        ),
    ]