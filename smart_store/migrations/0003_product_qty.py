# Generated by Django 5.2.1 on 2025-06-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_store', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
