# Generated by Django 4.1.7 on 2023-07-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_status_remove_order_tracking_dlivery_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
