# Generated by Django 4.1.7 on 2023-07-23 19:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0018_reviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='reviews',
            new_name='review',
        ),
    ]
