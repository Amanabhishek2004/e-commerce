# Generated by Django 4.1.7 on 2023-08-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_delete_customer'),
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='Orders_till_now',
            field=models.ManyToManyField(null=True, to='base.orders'),
        ),
        migrations.AddField(
            model_name='customer',
            name='activities',
            field=models.ManyToManyField(null=True, to='base.review'),
        ),
    ]
