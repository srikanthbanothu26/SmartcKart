# Generated by Django 5.2.1 on 2025-06-06 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_store', '0011_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smart_store.order')),
            ],
        ),
    ]
