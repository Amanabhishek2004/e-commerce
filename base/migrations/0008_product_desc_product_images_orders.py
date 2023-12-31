# Generated by Django 4.1.7 on 2023-07-15 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_product_for_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(null=True, upload_to='shop/images'),
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliver_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.address')),
            ],
        ),
    ]
