# Generated by Django 5.2.1 on 2025-06-06 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_store', '0007_cart_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
