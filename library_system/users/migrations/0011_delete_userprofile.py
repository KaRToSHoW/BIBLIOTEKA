# Generated by Django 5.0.6 on 2024-06-06 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]