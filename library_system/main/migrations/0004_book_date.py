# Generated by Django 5.0.6 on 2024-06-05 15:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_book_description_delete_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]